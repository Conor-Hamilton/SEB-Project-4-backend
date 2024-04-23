# controllers/classAttendeeController.py
from flask import Blueprint, request, jsonify, g
from models.classAttendee import ClassAttendee
from models.classes import ClassModel
from serializers.classAttendeeSchema import ClassAttendeeSchema
from app import db
from middleware.secureRoute import secure_route
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from datetime import datetime, timezone

class_attendee_controller = Blueprint("class_attendees", __name__)
class_attendee_schema = ClassAttendeeSchema()


# Register a user for a class
@class_attendee_controller.route("/class_attendees", methods=["POST"])
@secure_route
def create_class_attendee():
    attendee_data = request.get_json()
    try:
        # Admins can register anyone, users can only register themselves
        if (
            not g.current_user.is_admin
            and attendee_data["user_id"] != g.current_user.id
        ):
            return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

        new_attendee = class_attendee_schema.load(attendee_data)
        db.session.add(new_attendee)
        db.session.commit()
        return class_attendee_schema.jsonify(new_attendee), HTTPStatus.CREATED
    except ValidationError as e:
        return {"errors": e.messages}, HTTPStatus.BAD_REQUEST


# Unregister a user from a class
@class_attendee_controller.route("/class_attendees/<int:id>", methods=["DELETE"])
@secure_route
def delete_class_attendee(id):
    attendee = ClassAttendee.query.get_or_404(id)
    if g.current_user.is_admin or attendee.user_id == g.current_user.id:
        db.session.delete(attendee)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    else:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED


# Get all attendees for a specific class
@class_attendee_controller.route("/classes/<int:class_id>/attendees", methods=["GET"])
def get_class_attendees(class_id):
    attendees = ClassAttendee.query.filter_by(class_id=class_id).all()
    return jsonify(class_attendee_schema.dump(attendees, many=True)), HTTPStatus.OK


# Get all booked future classes for a user
@class_attendee_controller.route("/class_attendees/future", methods=["GET"])
@secure_route
def get_future_classes():
    current_user_id = g.current_user.id
    future_classes = (
        ClassAttendee.query.filter(
            ClassAttendee.user_id == current_user_id,
            ClassModel.start_time > datetime.now(timezone.utc),
        )
        .join(ClassModel)
        .all()
    )
    return jsonify(class_attendee_schema.dump(future_classes, many=True)), HTTPStatus.OK


# Get all past classes attended by a user
@class_attendee_controller.route("/class_attendees/past", methods=["GET"])
@secure_route
def get_past_classes():
    current_user_id = g.current_user.id
    past_classes = (
        ClassAttendee.query.filter(
            ClassAttendee.user_id == current_user_id,
            ClassModel.start_time <= datetime.now(timezone.utc),
        )
        .join(ClassModel)
        .all()
    )
    return jsonify(class_attendee_schema.dump(past_classes, many=True)), HTTPStatus.OK
