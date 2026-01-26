from datetime import datetime

from flask_jwt_extended import get_jwt_identity
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from app.dao.base_dao import BaseDao
from app.extension import db
from app.models import User
from app.models.scopes import UserScopes
from config.logging import logger


class UserDao(BaseDao):
    """Handles direct database operations"""

    def find_one(include_deleted=False, **filters):
        """
        To Search specific column
        """
        query = User.query

        if not include_deleted:
            query = query.filter(User.deleted_at.is_(None))

        return query.filter_by(**filters).first()

    def is_valid_user(email: str):
        """
        Search unlock user with email
        """
        return User.query.filter_by(
            email=email, deleted_at=None, lock_flg=False
        ).first()

    def paginate(filters, page: int, per_page: int):
        """
        Paginate User records with optional filters for name, email, role, and creation date.
        """
        user_id = get_jwt_identity()
        query = User.query

        # --- Apply scopes from UserScopes ---
        query = UserScopes.active(query, exclude_user_id=user_id)
        query = UserScopes.filter_name_email(query, filters)
        query = UserScopes.filter_role(query, filters)
        query = UserScopes.filter_date(query, filters)

        return query.order_by(User.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def create(user: User):
        db.session.add(user)
        return user

    def get_user(user_id: int):
        return (
            User.query.options(joinedload(User.creator), joinedload(User.updater))
            .filter_by(id=user_id, deleted_at=None, lock_flg=False)
            .first()
        )

    def update():
        db.session.commit()

    def delete_users(user_ids: list[int]):
        """
        Delete users by user_ids
        """
        users = User.query.filter(
            User.id.in_(user_ids), User.deleted_at.is_(None)
        ).all()
        for user in users:
            user.soft_delete()
        db.session.commit()
        return users

    def lock_users(user_ids: list[int]):
        """_ Lock multiple users by updating lock_flg, lock_count, last_lock_at_

        Args:
            user_ids (list[int]): _users ids_

        Returns:
            _list[int]_: _locked users_
        """
        users = User.query.filter(
            User.id.in_(user_ids), User.deleted_at.is_(None)
        ).all()
        for user in users:
            user.lock_flg = True
            user.lock_count = (user.lock_count or 0) + 1
            user.last_lock_at = datetime.utcnow()
        db.session.commit()
        return users

    def unlock_users(user_ids: list[int]):
        """_ unLock multiple users by updating lock_flg, last_lock_at_

        Args:
            user_ids (list[int]): _users ids_

        Returns:
            _list[int]_: _unlocked users_
        """
        users = User.query.filter(
            User.id.in_(user_ids), User.deleted_at.is_(None)
        ).all()
        for user in users:
            user.lock_flg = False
            user.last_lock_at = None
        db.session.commit()
        return users
