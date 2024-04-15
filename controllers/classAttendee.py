from flask import Blueprint, request, jsonify
from models.classAttendee import ClassAttendee
from serializers.classAttendeeSchema import ClassAttendeeSchema
from app import db
from http import HTTPStatus

class_attendee_controller = Blueprint("class_attendees", __name__)
class_attendee_schema = ClassAttendeeSchema()
