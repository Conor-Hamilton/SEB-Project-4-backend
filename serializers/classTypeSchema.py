from app import marsh
from models.classType import ClassType


class ClassTypeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ClassType
        load_instance = True
