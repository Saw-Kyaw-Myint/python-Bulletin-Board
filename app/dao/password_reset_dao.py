from app.dao.base_dao import BaseDao
from app.extension import db
from app.models.password_reset import PasswordReset


class PasswordResetDao(BaseDao):

    def create_password_reset(payload, token):
        """
        Insert email and token
        """
        reset = PasswordReset(
            email=payload.email,
            token=token,
        )
        db.session.add(reset)
        return reset

    def find_one(include_deleted: bool = False, **filters):
        """
        To Search specific column
        """
        query = PasswordReset.query

        if not include_deleted:
            query = query.filter(PasswordReset.deleted_at.is_(None))

        return query.filter_by(**filters).first()
