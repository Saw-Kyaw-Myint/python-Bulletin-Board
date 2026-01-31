import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str
    remember: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not v:
            return v
        if not re.fullmatch(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,20}", v):
            raise ValueError(
                "Password must be 6–20 chars and include upper, lower, number, and special character"
            )
        return v

    @classmethod
    def messages(cls):
        return {
            "email.missing": "The Email Address field is required.",
            "email.value_error": "The Email Address field format is invalid.",
            "email.too_long": "The Email may not be greater than 50 characters.",
            "password.missing": "The Password field is required.",
            "password.value_error": "The Password must be 6-20 chars and can include letters, digits, and special chars.",
        }
