from http import HTTPStatus
import logging
from flask import Blueprint, request, jsonify, g
from models.classes import ClassModel
from serializers.classSchema import ClassesSerializer
from middleware.secureRoute import secure_route
from app import db
from marshmallow.exceptions import ValidationError
from datetime import datetime, time

classes_controller = Blueprint("classes", __name__)
class_schema = ClassesSerializer()


# Creating a class
@classes_controller.route("/classes", methods=["POST"])
@secure_route
def create_class():
    class_data = request.get_json()

    if not (g.current_user.is_admin or g.current_user.is_coach):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        class_ = class_schema.load(class_data)
        class_.creator = g.current_user
        db.session.add(class_)
        db.session.commit()
        return class_schema.jsonify(class_), HTTPStatus.CREATED

    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        logging.exception("An error occurred while creating a class.")
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR


# Getting all classes
@classes_controller.route("/classes", methods=["GET"])
def get_classes():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    query = ClassModel.query

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(ClassModel.start_time >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date_with_time = datetime.combine(end_date, time(23, 59, 59))
        query = query.filter(ClassModel.end_time <= end_date_with_time)

    classes = query.all()
    return jsonify(class_schema.dump(classes, many=True)), HTTPStatus.OK


# Updating a class
@classes_controller.route("/classes/<int:class_id>", methods=["PUT"])
@secure_route
def update_class(class_id):
    class_ = ClassModel.query.get(class_id)

    if not class_:
        return {"message": "Class not found"}, HTTPStatus.NOT_FOUND
    if not (
        g.current_user.is_admin
        or (g.current_user.is_coach and g.current_user.id == class_.creator_id)
    ):
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        class_data = request.get_json()
        class_ = class_schema.load(class_data, instance=class_, partial=True)
        db.session.commit()
        return class_schema.jsonify(class_), HTTPStatus.OK

    except ValidationError as e:
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    except Exception as e:
        logging.exception("An error occurred while updating a class.")
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR


# Deleting a class
@classes_controller.route("/classes/<int:class_id>", methods=["DELETE"])
@secure_route
def delete_class(class_id):
    class_ = ClassModel.query.get(class_id)

    if not class_:
        return {"message": "Class not found"}, HTTPStatus.NOT_FOUND

    if not g.current_user.is_admin:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

    try:
        db.session.delete(class_)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT

    except Exception as e:
        logging.exception("An error occurred while deleting a class.")
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
