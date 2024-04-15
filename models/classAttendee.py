from app import db


class ClassAttendee(db.Model):
    __tablename__ = "class_attendees"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel", backref="attended_classes")
    class_ = db.relationship("ClassModel", backref="attendees")
