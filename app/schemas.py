
from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=15)
    email: EmailStr
    subject: str = Field(min_length=2, max_length=100)
    message: str = Field(min_length=5, max_length=2000)
