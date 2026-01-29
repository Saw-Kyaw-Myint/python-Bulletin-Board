# app/models/scopes/user_scopes.py
from datetime import datetime

from sqlalchemy import or_

from app.models import User
from app.utils.decorators import static_all_methods
from config.logging import logger


@static_all_methods
class UserScopes:
    """
    Reusable query scopes for the User model.
    """

    def active(query, exclude_user_id=None):
        """Filter out deleted users and optionally exclude the current user."""
        query = query.filter(User.deleted_at.is_(None))
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query

    def filter_name_email(query, filters):
        """Filter users by name and/or email (case-insensitive partial match)."""
        name = (filters.get("name") or "").strip()
        email = (filters.get("email") or "").strip()
        if name or email:
            conditions = []
            if name:
                conditions.append(User.name.like(f"%{name}%"))
            if email:
                conditions.append(User.email.like(f"%{email}%"))
            query = query.filter(or_(*conditions))
        return query

    def filter_role(query, filters):
        """Filter users by role if provided."""
        role = filters.get("role")
        if role is not None:
            query = query.filter(User.role == role)
        return query

    def filter_date(query, filters):
        """Filter users by creation date range."""
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        try:
            if start_date:
                start = datetime.fromisoformat(start_date)
                query = query.filter(User.created_at >= start)
            if end_date:
                end = datetime.fromisoformat(end_date)
                query = query.filter(User.created_at <= end)
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
        return query

    def latest(query):
        """Order users by latest."""
        return query.order_by(User.id.desc())
