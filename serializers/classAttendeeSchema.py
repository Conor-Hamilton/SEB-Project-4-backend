from app import marsh
from models.classAttendee import ClassAttendee
from marshmallow import fields


class ClassAttendeeSchema(marsh.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer", only=("id", "username"), many=False)
    class_ = fields.Nested(
        "ClassesSerializer", only=("id", "title", "start_time", "description"), many=False
    )

    class Meta:
        model = ClassAttendee
        load_instance = True
        include_fk = True
