import random
import string
from datetime import timedelta, datetime
from humanfriendly import format_timespan
from data.repositories.repository_impl import IRepository


class GatePassService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def generate_gate_pass(self, current_user: dict, data: dict) -> dict:
        expiration_minutes = int(data["expiration"])
        if expiration_minutes <= 0:
            raise ValueError("Invalid expiration value.")
        self.repository.delete_tokens(current_user["email"])  # Invalidate previous tokens
        token_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        expires_at = datetime.now() + timedelta(minutes=expiration_minutes)
        token_data = {
            "token_id": token_id,
            "visitor_name": data["visitor_name"],
            "visitor_phone": data["visitor_phone"],
            "expires_at": expires_at,
            "resident_id": current_user["email"],
            "is_active": True,
            "purpose": "entry",
        }
        self.repository.insert_token(token_data)
        time_to_expire = format_timespan(expiration_minutes * 60)
        return {"token_id": token_id, "expires_in": time_to_expire}

    def validate_gate_pass(self, token_id: str, current_user: dict) -> dict:
        token = self.repository.find_token_by_id(token_id)
        if not token or token["resident_id"] != current_user["email"]:
            raise ValueError("Token not found or unauthorized.")
        if datetime.utcnow() > token["expires_at"]:
            raise ValueError("Token has expired.")
        return {
            "visitor_name": token["visitor_name"],
            "visitor_phone": token["visitor_phone"],
            "expires_at": token["expires_at"].isoformat(),
            "purpose": token.get("purpose", "entry"),
        }

    def generate_exit_gate_pass(self, token_id: str, current_user: dict) -> dict:
        token = self.repository.find_token_by_id(token_id)
        if not token or token["resident_id"] != current_user["email"]:
            raise ValueError("Token not found or unauthorized.")
        self.repository.invalidate_token(token_id)  # Invalidate the current token
        exit_token_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exit_expires_at = datetime.now() + timedelta(minutes=15)
        exit_token_data = {
            "token_id": exit_token_id,
            "visitor_name": token["visitor_name"],
            "visitor_phone": token["visitor_phone"],
            "expires_at": exit_expires_at,
            "resident_id": current_user["email"],
            "is_active": True,
            "purpose": "exit",
        }
        self.repository.insert_token(exit_token_data)
        time_to_expire = format_timespan(15 * 60)
        return {"exit_token_id": exit_token_id, "expires_in": time_to_expire}