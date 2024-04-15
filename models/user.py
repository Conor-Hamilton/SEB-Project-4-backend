from sqlalchemy.ext.hybrid import hybrid_property
from app import db, bcrypt
from associations import users_user_types

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=True)
    user_types = db.relationship(
        "UserType", secondary="users_user_types", back_populates="users"
    )

    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password).decode(
            "utf-8"
        )

    def validate_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)

    @hybrid_property
    def is_admin(self):
        return any(u_type.name == 'Admin' for u_type in self.user_types)

    @hybrid_property
    def is_coach(self):
        return any(u_type.name == 'Coach' for u_type in self.user_types)
