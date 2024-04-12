from app import db
from models.user import UserModel

class CoachModel(db.Model):
    __tablename__ = "coaches"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    
    user = db.relationship('UserModel', back_populates='coach', uselist=False)
