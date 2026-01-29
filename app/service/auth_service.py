from datetime import datetime, timezone

from flask_bcrypt import check_password_hash
import secrets
from app.dao.user_dao import UserDao
from app.service.base_service import BaseService
from app.shared.commons import field_error
from app.dao.password_reset_dao import PasswordResetDao


class AuthService(BaseService):
    def login(payload):
        """
        Login and update last_login_at
        """
        user = UserDao.is_valid_user(payload.email)
        if not user:
            field_error(
                "email", "The Selected Email address doesn't exist or invalid.", 400
            )

        if not check_password_hash(user.password, payload.password):
            field_error("password", "The Password Field is required.", 400)
        user.last_login_at = datetime.now(timezone.utc)

        return user
    
    def forgot_password(payload):
        """
        Remove Token and insert token to DB
        """
        user = UserDao.is_valid_user(payload.email)
        if not user:
            field_error(
                "email", "The Selected Email address doesn't exist or invalid.", 400
            )
        token = secrets.token_urlsafe(16)
        PasswordResetDao.remove_token_by_email(payload.email)
        PasswordResetDao.create_password_reset(payload,token)

        return token
            
        
