from datetime import timedelta, datetime
import jwt
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from data.repositories.repository_impl import IRepository
from helpers.db_config import Config


class AuthService:
    def __init__(self, repository: IRepository, secret_key: str):
        self.repository = repository
        self.secret_key = secret_key

    def register_user(self, data: dict) -> dict:
        payload = {
            "user_data": {
                "fullname": data["fullname"],
                "email": data["email"],
                "phone": data["phone"],
                "status": data.get("status", "Visitor"),
            },
            "exp": datetime.now() + timedelta(days=2),
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        verification_link = f"{Config.FRONTEND_URL}/api/verify/{token}"
        return {"message": "Verification email sent.", "token": token, "verification_link": verification_link}

    def verify_user(self, token: str, password: str) -> dict:
        decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        if datetime.now().timestamp() > decoded.get("exp", 0):
            raise ValueError("Token expired.")
        user_data = decoded["user_data"]
        if self.repository.get_user_by_email(user_data["email"]):
            raise ValueError("Email already registered.")
        hashed_password = generate_password_hash(password)
        user_data.update({"password": hashed_password, "is_active": True})
        self.repository.insert_user(user_data)
        return {
            "access_token": create_access_token(identity=user_data["email"]),
            "refresh_token": create_refresh_token(identity=user_data["email"]),
        }

    def login_user(self, email: str, password: str) -> dict:
        user = self.repository.get_user_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            raise ValueError("Invalid credentials.")
        return {
            "access_token": create_access_token(identity=user["email"], expires_delta=timedelta(days=1)),
            "refresh_token": create_refresh_token(identity=user["email"]),
        }