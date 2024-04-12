from app import db


class ClassType(db.Model):

    __tablename__ = "class_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    classes = db.relationship("ClassModel", backref="class_type", lazy=True)
