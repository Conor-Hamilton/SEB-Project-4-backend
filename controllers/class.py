from flask import Blueprint, request, jsonify
from models.classes import ClassModel
from serializers.classSchema import ClassSchema
from app import db
from marshmallow.exceptions import ValidationError
from http import HTTPStatus

classes_controller = Blueprint("classes", __name__)
class_schema = ClassSchema()
