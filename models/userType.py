from app import db


class UserType(db.Model):
    __tablename__ = "user_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  
    isAdmin = db.Column(db.Boolean, default=False)
    isCustomer = db.Column(db.Boolean, default=False)
    isCoach = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="user_types")
