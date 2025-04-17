from datetime import datetime, timedelta, timezone
from typing import Optional
from app.core.security import verify_password, create_access_token, generate_otp
from app.db.mongodb import get_user_collection, get_otp_collection
from app.models.user import UserInDB
from app.config import settings

async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    user_dict = await user_collection.find_one({"email": email})
    if not user_dict:
        return None
    user = UserInDB(**user_dict)
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def create_otp_for_user(email: str) -> str:
    otp_collection = get_otp_collection()
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
    
    # Delete any existing OTP for this email
    await otp_collection.delete_many({"email": email})
    
    # Create new OTP record
    await otp_collection.insert_one({
        "email": email,
        "otp": otp,
        "expires_at": expires_at,
        "created_at": datetime.now(timezone.utc)
    })
    
    return otp

async def verify_otp(email: str, otp: str) -> bool:
    otp_collection = get_otp_collection()
    otp_record = await otp_collection.find_one({
        "email": email,
        "otp": otp,
        "expires_at": {"$gt": datetime.now(timezone.utc)}
    })
    
    if otp_record:
        # Delete the OTP after successful verification
        await otp_collection.delete_one({"_id": otp_record["_id"]})
        return True
    return False