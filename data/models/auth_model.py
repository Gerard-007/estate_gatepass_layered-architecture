from datetime import datetime

from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField


class User(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, max_length=11)
    status = StringField(default="Resident", choices=["Resident", "Admin", "Security"])
    password = StringField(required=False)
    is_active = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now())
    meta = {"collection": "users", "db_alias": "default"}


class RevokedToken(Document):
    jti = StringField(required=True, unique=True)
    meta = {
        "collection": "revoked_tokens",
        "indexes": ["jti"]
    }