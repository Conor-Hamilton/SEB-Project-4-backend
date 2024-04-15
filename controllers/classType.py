from flask import Blueprint, request, jsonify
from models.classType import ClassType
from serializers.classTypeSchema import ClassTypeSchema
from app import db
from http import HTTPStatus

class_type_controller = Blueprint("class_types", __name__)
class_type_schema = ClassTypeSchema()
