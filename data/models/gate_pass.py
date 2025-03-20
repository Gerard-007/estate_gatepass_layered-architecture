from datetime import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField

from data.models.auth_model import User


class VisitorToken(Document):
    token_id = StringField(primary_key=True, max_length=6)
    visitor_name = StringField(required=True)
    visitor_phone = StringField(required=True)
    expires_at = DateTimeField(required=True)
    resident = ReferenceField(User, required=True)
    is_active = BooleanField(default=True)
    purpose = StringField(choices=["entry", "exit"], default="entry")
    created_at = DateTimeField(default=datetime.now())
    meta = {"collection": "gate_pass"}