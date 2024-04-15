from app import db
from associations import users_user_types

class UserType(db.Model):
    __tablename__ = "user_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship(
        "UserModel", secondary="users_user_types", back_populates="user_types"
    )
