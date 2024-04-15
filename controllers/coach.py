from flask import Blueprint, request, jsonify
from models.coach import CoachModel
from serializers.coachSchema import CoachSchema
from app import db
from http import HTTPStatus

coach_controller = Blueprint("coaches", __name__)
coach_schema = CoachSchema()

