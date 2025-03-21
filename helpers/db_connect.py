from mongoengine import connect
from data.repositories.repository import MongoRepository
from helpers.config import Config
from services.auth_service import AuthService
from services.gate_pass_service import GatePassService


def initialize_db():
    try:
        connect(host=f"{Config.MONGO_URI}/{Config.DB_NAME}", alias="default")
        print(f"Connected to {Config.DB_NAME}!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        exit(1)


auth_repository = MongoRepository(collection_name=Config.AUTH_COLLECTION)
gatepass_repository = MongoRepository(collection_name=Config.GATEPASS_COLLECTION)


auth_service = AuthService(repository=auth_repository, secret_key=Config.JWT_SECRET_KEY)
gate_pass_service = GatePassService(repository=gatepass_repository)