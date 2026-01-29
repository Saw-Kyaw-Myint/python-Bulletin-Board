from app.dao.base_dao import BaseDao
from app.models.password_reset import PasswordReset
from app.extension import db

class PasswordResetDao(BaseDao):

    def create_password_reset(payload,token):
        """
        Insert email and token
        """
        reset = PasswordReset(
        email=payload.email,
        token=token,
        )
        db.session.add(reset)
        return reset
 
    def remove_token_by_email(email):
        """
        Remove previous Token
        """
        return PasswordReset.query.filter_by(email=email).delete()
        
