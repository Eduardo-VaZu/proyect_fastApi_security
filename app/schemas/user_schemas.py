from pydantic import Field, EmailStr, BaseModel, field_validator
import re


class RequestUserSchemas(BaseModel):
    """
    Schema for validating user registration data.
    """

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        """
        Validate password complexity requirements:
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one digit
        - At least one special character (@$!%*?&)
        """
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError(
                "Password must contain at least one special character (@$!%*?&)"
            )
        return value


class ResponseUserSchemas(BaseModel):
    """
    Schema for user information returned in API responses.
    """

    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
