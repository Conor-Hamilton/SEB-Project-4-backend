from app import marsh
from models.userType import UserType


class UserTypeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        load_instance = True
