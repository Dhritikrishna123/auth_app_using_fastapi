from app.core.auth import create_otp_for_user, verify_otp
from app.services.email_service import send_otp_email
from app.services.user_service import mark_email_verified

async def generate_and_send_otp(email: str):
    otp = await create_otp_for_user(email)
    success = await send_otp_email(email, otp)
    return success

async def verify_otp_and_activate(email: str, otp: str):
    is_valid = await verify_otp(email, otp)
    if is_valid:
        await mark_email_verified(email)
    return is_valid