from app import marsh
from models.coach import CoachModel
from marshmallow import fields


class CoachSchema(marsh.SQLAlchemyAutoSchema):
    user = fields.Nested("UserSerializer", only=("id", "username", "email"), many=False)

    class Meta:
        model = CoachModel
        load_instance = True
        include_fk = True  
