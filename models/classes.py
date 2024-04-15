from app import db


class ClassModel(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    class_type_id = db.Column(
        db.Integer, db.ForeignKey("class_types.id"), nullable=False
    )

    creator = db.relationship("UserModel", backref="created_classes")
