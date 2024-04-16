# controllers/classTypeController.py
from flask import Blueprint, request, jsonify, g
from models.classType import ClassType
from serializers.classTypeSchema import ClassTypeSchema
from app import db
from middleware.secureRoute import secure_route
from marshmallow.exceptions import ValidationError
from http import HTTPStatus

class_type_controller = Blueprint("class_types", __name__)
class_type_schema = ClassTypeSchema()


# Create a new class type
@class_type_controller.route("/class_types", methods=["POST"])
@secure_route
def create_class_type():
    if not (g.current_user.is_admin or g.current_user.is_coach):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        class_type_data = request.get_json()
        class_type = class_type_schema.load(class_type_data)
        db.session.add(class_type)
        db.session.commit()
        return class_type_schema.jsonify(class_type), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"errors": e.messages}), HTTPStatus.BAD_REQUEST


# Get all class types
@class_type_controller.route("/class_types", methods=["GET"])
def get_class_types():
    class_types = ClassType.query.all()
    return class_type_schema.jsonify(class_types, many=True), HTTPStatus.OK


# Get a single class type by ID
@class_type_controller.route("/class_types/<int:id>", methods=["GET"])
def get_class_type(id):
    class_type = ClassType.query.get_or_404(id)
    return class_type_schema.jsonify(class_type), HTTPStatus.OK


# Update a class type
@class_type_controller.route("/class_types/<int:id>", methods=["PUT"])
@secure_route
def update_class_type(id):
    if not (g.current_user.is_admin or g.current_user.is_coach):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    class_type = ClassType.query.get_or_404(id)
    try:
        class_type_data = request.get_json()
        class_type = class_type_schema.load(
            class_type_data, instance=class_type, partial=True
        )
        db.session.commit()
        return class_type_schema.jsonify(class_type), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"errors": e.messages}), HTTPStatus.UNPROCESSABLE_ENTITY


# Delete a class type
@class_type_controller.route("/class_types/<int:id>", methods=["DELETE"])
@secure_route
def delete_class_type(id):
    if not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    class_type = ClassType.query.get_or_404(id)
    db.session.delete(class_type)
    db.session.commit()
    return jsonify({}), HTTPStatus.NO_CONTENT
