from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(min_length=3, max_length=150)
    last_name: str = Field(min_length=3, max_length=150)
    email: EmailStr
    phone_number: str = Field(pattern=r"^\+380\d{9}$")
    birthday: date
    additional_info: Optional[str]


class ContactResponse(ContactModel):
    id: int


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=4, max_length=12)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class ResetPasswordModel(BaseModel):
    password1: str = Field(min_length=4, max_length=12)
    password2: str = Field(min_length=4, max_length=12)