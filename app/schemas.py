
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str
    email: EmailStr
    subject: str = Field(min_length=2, max_length=100)
    message: str = Field(min_length=5, max_length=2000)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\+?[0-9]{10,15}", value):
            raise ValueError(
                "Phone number must contain 10-15 digits "
                "and may start with +"
            )
        return value

    @field_validator("name", "subject", "message")
    @classmethod
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("This field cannot be empty")
        return value.strip()
