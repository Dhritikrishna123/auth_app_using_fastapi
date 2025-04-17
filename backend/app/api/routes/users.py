from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional
import shutil
import os
from app.dependencies import get_current_active_user
from app.models.user import UserInDB
from app.schemas.user import UserResponse, AddressUpdate
from app.services.user_service import update_user, update_user_address

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        phone_number=current_user.phone_number,
        license_plate_number=current_user.license_plate_number,
        address=current_user.address,
        profile_pic_url=current_user.profile_pic_url,
        email_verified=current_user.email_verified,
        phone_verified=current_user.phone_verified
    )

@router.put("/me/address", response_model=UserResponse)
async def update_address(
    address_data: AddressUpdate,
    current_user: UserInDB = Depends(get_current_active_user)
):
    try:
        updated_user = await update_user_address(
            str(current_user.id),
            latitude=address_data.latitude,
            longitude=address_data.longitude,
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            country=address_data.country,
            postal_code=address_data.postal_code
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(updated_user.id),
            name=updated_user.name,
            email=updated_user.email,
            phone_number=updated_user.phone_number,
            license_plate_number=updated_user.license_plate_number,
            address=updated_user.address,
            profile_pic_url=updated_user.profile_pic_url,
            email_verified=updated_user.email_verified,
            phone_verified=updated_user.phone_verified
        )
    except Exception as e:
        print(f"Error in update_address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address"
        )

@router.post("/me/profile-picture", response_model=UserResponse)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads/profile_pics", exist_ok=True)
    
    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    file_path = f"uploads/profile_pics/{current_user.id}.{file_extension}"
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update the user's profile picture URL
    profile_pic_url = f"/uploads/profile_pics/{current_user.id}.{file_extension}"
    updated_user = await update_user(
        str(current_user.id),
        {"profile_pic_url": profile_pic_url}
    )
    
    return UserResponse(
        id=str(updated_user.id),
        name=updated_user.name,
        email=updated_user.email,
        phone_number=updated_user.phone_number,
        license_plate_number=updated_user.license_plate_number,
        address=updated_user.address,
        profile_pic_url=updated_user.profile_pic_url,
        email_verified=updated_user.email_verified,
        phone_verified=updated_user.phone_verified
    )