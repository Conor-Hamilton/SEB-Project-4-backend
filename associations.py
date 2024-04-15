from app import db

users_user_types = db.Table(
    "users_user_types",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "user_type_id", db.Integer, db.ForeignKey("user_types.id"), primary_key=True
    ),
)
