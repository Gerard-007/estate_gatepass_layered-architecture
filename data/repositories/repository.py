from mongoengine import DoesNotExist

from data.models.auth_model import User
from data.models.gate_pass import VisitorToken
from data.repositories.repository_impl import IRepository


class MongoRepository(IRepository):
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.switch_collection()

    def switch_collection(self):
        if self.collection_name == "users":
            self.collection = User
        elif self.collection_name == "gate_pass":
            self.collection = VisitorToken

    def get_user_by_email(self, email: str) -> dict:
        return User.objects(email=email).first()

    def insert_user(self, user_data: dict) -> str:
        user = User(**user_data).save()
        return str(user.id)

    def delete_tokens(self, resident_id: str) -> None:
        VisitorToken.objects(resident=resident_id, is_active=True).delete()

    def find_token_by_id(self, token_id: str) -> dict:
        return VisitorToken.objects(token_id=token_id, is_active=True).first()

    def invalidate_token(self, token_id: str) -> None:
        try:
            VisitorToken.objects(token_id=token_id).update(set__is_active=False)
        except DoesNotExist:
            pass

    def insert_token(self, token_data: dict) -> str:
        token = VisitorToken(**token_data).save()
        return str(token.id)
