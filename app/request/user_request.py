# app/request/user_request.py
from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, constr, validator

from app.shared.commons import field_error
from config.logging import logger

NonEmptyStr = constr(min_length=1, strip_whitespace=True)


class UserCreateRequest(BaseModel):
    """
    Schema for validating user creation requests.
    """

    name: NonEmptyStr
    email: EmailStr = Field(..., max_length=50)
    password: str

    @validator("password")
    def strong_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError("Password must be 6-20 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must include at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must include at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must include at least one number")
        if not any(c in "@$!%*?&" for c in v):
            raise ValueError(
                "Password must include at least one special character @$!%*?&"
            )
        return v

    confirm_password: NonEmptyStr
    role: int = Field(..., ge=0, le=1)
    phone: Optional[str] = None
    dob: Optional[date | str] = None
    profile: Optional[Any] = None
    address: NonEmptyStr

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("profile")
    def file_required(cls, v):
        if not v:
            raise ValueError("The Profile field is required")
        return v

    @classmethod
    def messages(cls):
        return {
            "name.missing": "The Name field is required.",
            "email.missing": "The Name field is required.",
            "email.value_error": "The Email Address field format is invalid.",
            "email.too_long": "The Email may not be greater than 50 characters.",
            "password.missing": "The Password field is required.",
            "password.string_too_short": "The Password must be at least 6 characters.",
            "password.string_too_long": "The Password may not be greater than 20 characters.",
            "password.string_pattern_mismatch": "The Password must be 8-20 chars and can include letters, digits, and special chars.",
            "confirm_password.missing": "The Password Confirm field is required.",
            "role.missing": "The Role field is required.",
            "address.missing": "The Address field is required.",
            "profile.value_error": "The Profile field is required.",
        }


class UserUpdateRequest(BaseModel):
    name: str = Field(None, min_length=3, max_length=50)
    email: EmailStr
