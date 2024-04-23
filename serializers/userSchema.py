from marshmallow import fields
from app import marsh
from models.user import UserModel
from marshmallow import validates, ValidationError


class UserSerializer(marsh.SQLAlchemyAutoSchema):
    password = fields.String(required=True)


    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password", "password_hash", "email")

    @validates('password')
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        if not any(c.isdigit() for c in value):
            raise ValidationError('Password must include at least one digit.')
        if not any(c.isupper() for c in value):
            raise ValidationError('Password must include at least one uppercase letter.')
        if not any(c.islower() for c in value):
            raise ValidationError('Password must include at least one lowercase letter.')
        if not any(c in "!@#$%^&*()-_+=" for c in value):
            raise ValidationError('Password must include at least one special character.')
