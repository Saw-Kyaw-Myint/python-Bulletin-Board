import os

from flask import jsonify, request
from werkzeug.utils import secure_filename

from app.request.user_request import UserCreateRequest, UserUpdateRequest
from app.schema.user_list_schema import UserListSchema
from app.schema.user_schema import UserSchema
from app.service.user_service import UserService
from app.shared.commons import field_error, validate_request
from config.logging import logger

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_list = UserListSchema(many=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def get_users():
    filters = {
        "name": request.args.get("name", type=str),
        "email": request.args.get("email", type=str),
        "role": request.args.get("role", type=int),
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
    }

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = UserService.filter_paginate(filters, page, per_page)

    return jsonify(
        {
            "data": user_list.dump(pagination.items),
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }
    )


@validate_request(UserCreateRequest)
def create_user(payload):
    file = request.files.get("profile")
    if not file:
        field_error("profile", "The Profile field is required", 422)
    UPLOAD_DIR = "public/images/profile"
    payload_dict = payload.model_dump()
    user_id = payload_dict["user_id"]
    user_dir = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower().lstrip(".")

    if ext not in ALLOWED_EXTENSIONS:
        field_error("profile", "The profile must be a file  of type.jpg,png", 422)

    original_filename = secure_filename(file.filename)
    file_path = os.path.join(user_dir, original_filename)

    payload_dict["profile"] = f"profile/{user_id}/{original_filename}"
    try:
        user = UserService.create(payload_dict)
        file.save(file_path)
    except ValueError as e:
        return jsonify({"message": str(e)}), 409

    return (
        jsonify(
            {
                "message": "Register success",
            }
        ),
        201,
    )


def show_user(user_id):
    user = UserService.get_user(user_id)
    return jsonify(user_schema.dump(user)), 200


# Update user
@validate_request(UserUpdateRequest)
def update_user(payload, id):
    file = request.files.get("profile")
    payload_dict = payload.model_dump()
    logger.info(payload_dict)
    if file:
        UPLOAD_DIR = "public/images/profile"
        user_id = payload_dict["user_id"]
        user_dir = os.path.join(UPLOAD_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        ext = os.path.splitext(file.filename)[1].lower().lstrip(".")

        if ext not in ALLOWED_EXTENSIONS:
            field_error("profile", "The profile must be a file  of type.jpg,png", 422)

        original_filename = secure_filename(file.filename)
        file_path = os.path.join(user_dir, original_filename)
        payload_dict["profile"] = f"profile/{user_id}/{original_filename}"

    try:
        user = UserService.update(payload_dict, id)
        if file:
            file.save(file_path)
    except ValueError as e:
        return jsonify({"message": str(e)}), 409

    return (
        jsonify(
            {
                "message": "user update is success",
                "user": {"id": user.id, "name": user.name, "email": user.email},
            }
        ),
        201,
    )


def delete_users():
    """_Delete users_

    Returns:
        _json_: _Error or Success_
    """
    data = request.get_json() or {}
    user_ids = data.get("user_ids")
    if not isinstance(user_ids, list) or not user_ids:
        return jsonify({"msg": "Provide a list of user IDs"}), 400
    try:
        users = UserService.delete_users(user_ids)
        return jsonify({"msg": f"{len(users)} users deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


def lock_users():
    """_Lock users_

    Returns:
        _json_: _Error or Success_
    """
    data = request.get_json() or {}
    user_ids = data.get("user_ids")
    if not isinstance(user_ids, list) or not user_ids:
        return jsonify({"msg": "Provide a list of user IDs"}), 400
    try:
        users = UserService.lock_users(user_ids)
        return jsonify({"msg": f"{len(users)} users locked successfully"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


def unlock_users():
    """_Unlock users_

    Returns:
        _json_: _Error or Success_
    """
    data = request.get_json() or {}
    user_ids = data.get("user_ids")
    if not isinstance(user_ids, list) or not user_ids:
        return jsonify({"msg": "Provide a list of user IDs"}), 400
    try:
        users = UserService.unlock_users(user_ids)
        return jsonify({"msg": f"{len(users)} users unlocked successfully"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
