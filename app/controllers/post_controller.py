from flask import jsonify, request

from app.schema.post_schema import PostSchema
from app.service.post_service import PostService
from app.shared.commons import paginate_response
from config.logging import logger

posts_schema = PostSchema(many=True)
post_schema = PostSchema()


def post_list():
    """
    Return a paginated list of posts with optional filters.
    """
    filters = {
        "name": request.args.get("name", type=str),
        "description": request.args.get("description", type=str),
        "status": request.args.get("status", type=int),
        "date": request.args.get("date"),
    }
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    posts = PostService.filter_paginate(filters, page, per_page)

    return paginate_response(posts, posts_schema)


def delete_posts():
    """_Delete posts_

    Returns:
        _json_: _Error or Success_
    """
    data = request.get_json() or {}
    post_ids = data.get("post_ids")
    if not isinstance(post_ids, list) or not post_ids:
        return jsonify({"msg": "Provide a list of post IDs"}), 400
    try:
        posts = PostService.delete_posts(post_ids)

        return jsonify({"msg": f"{len(posts)} posts deleted successfully"}), 200
    except ValueError as e:
        logger.error("Post Controller : delete_posts")
        logger.error(e)
        return jsonify({"msg": str(e)}), 404


def show_post(post_id):
    """
    Get User by user id
    """
    post = PostService.get_post(post_id)
    return jsonify(post_schema.dump(post)), 200
