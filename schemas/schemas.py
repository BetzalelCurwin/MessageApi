from flask_marshmallow import Marshmallow
from marshmallow import EXCLUDE, ValidationError
from app.main import app
from models.models import Message

ma = Marshmallow(app)


def validate_strings(obj: str):
    if len(obj.strip()) == 0:
        raise ValidationError("string must not be empty")


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message
        unknown = EXCLUDE

    id = ma.auto_field()
    text = ma.auto_field(validate=validate_strings)
    subject = ma.auto_field(validate=validate_strings)
    created_at = ma.auto_field()
    sender_id = ma.auto_field()
    receiver_id = ma.auto_field()




