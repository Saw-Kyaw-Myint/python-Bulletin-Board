from app.dao.post_dao import PostDao
from app.service.base_service import BaseService


class PostService(BaseService):

    def filter_paginate(filters, page: int, per_page: int):
        """
        Filter posts and return paginated results.
        """
        posts = PostDao.paginate(filters, page, per_page)

        return posts

    def get_post(post_id: int):
        """
        Get post by post id
        """
        post = PostDao.get_post(post_id)
        if not post:
            return ValueError("User don't not exist.")
        return post

    def delete_posts(post_ids):
        """
        Delete posts by IDs.
        """
        posts = PostDao.delete_posts(post_ids)
        if not posts:
            raise ValueError("not user found")
        return posts
