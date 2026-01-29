from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., max_length=50)

    @classmethod
    def messages(cls):
        return {
            "email.missing": "The Email Address field is required.",
            "email.value_error": "The Email Address field format is invalid.",
            "email.too_long": "The Email may not be greater than 50 characters.",
        }
