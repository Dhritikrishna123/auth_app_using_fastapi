from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import Address, User

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone_number: str
    license_plate_number: str
    address: Optional[Address] = None
    profile_pic_url: Optional[str] = None
    email_verified: bool
    phone_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

class AddressUpdate(BaseModel):
    latitude: float
    longitude: float
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None