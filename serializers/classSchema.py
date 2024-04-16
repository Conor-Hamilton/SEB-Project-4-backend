from app import marsh
from models.classes import ClassModel
from serializers.userSchema import UserSerializer
from marshmallow import fields


class ClassesSerializer(marsh.SQLAlchemyAutoSchema):
    creator = fields.Nested(
        UserSerializer, only=("id", "username", "email"), many=False
    )

    class Meta:
        model = ClassModel
        load_instance = True
        include_fk = True
        exclude = ("creator_id",)
