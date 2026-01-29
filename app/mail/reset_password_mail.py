from flask_mail import Message
from flask import render_template
from app.extension import mail
from app.utils.decorators import static_all_methods
from config.mail import MailConfig
from config.logging import logger

@static_all_methods
class ResetPasswordMail:

    def send_reset_email(to_email, reset_url):
        """
        Send Mail
        """
        msg = Message(
            subject="Reset Your Password",
            recipients=[to_email]
        )

        msg.html = render_template(
            "emails/reset_password.html",
            reset_url=reset_url
        )

        mail.send(msg)