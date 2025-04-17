from datetime import datetime
from bson import ObjectId
from typing import Optional, List
from app.models.user import UserCreate, UserInDB, UserUpdate, User
from app.core.security import get_password_hash
from app.db.mongodb import get_user_collection

async def create_user(user_in: UserCreate) -> UserInDB:
    user_collection = get_user_collection()
    
    # Check if user with this email already exists
    existing_user = await user_collection.find_one({"email": user_in.email})
    if existing_user:
        raise ValueError("Email already registered")
    
    # Check if user with this phone already exists
    existing_phone = await user_collection.find_one({"phone_number": user_in.phone_number})
    if existing_phone:
        raise ValueError("Phone number already registered")
        
    user_dict = user_in.dict()
    hashed_password = get_password_hash(user_dict.pop("password"))
    
    db_user = UserInDB(
        **user_dict,
        hashed_password=hashed_password,
        is_active=True,
        email_verified=False,
        phone_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    result = await user_collection.insert_one(db_user.dict(by_alias=True))
    db_user.id = result.inserted_id
    
    return db_user

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    user_dict = await user_collection.find_one({"email": email})
    if user_dict:
        return UserInDB(**user_dict)
    return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    user_dict = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user_dict:
        return UserInDB(**user_dict)
    return None

async def update_user(user_id: str, user_update: UserUpdate) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Hash password if it's being updated
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        
        await user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    return await get_user_by_id(user_id)

async def mark_email_verified(email: str) -> bool:
    user_collection = get_user_collection()
    result = await user_collection.update_one(
        {"email": email},
        {"$set": {"email_verified": True, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

async def update_user_address(user_id: str, latitude: float, longitude: float, 
                             street: Optional[str] = None, city: Optional[str] = None,
                             state: Optional[str] = None, country: Optional[str] = None,
                             postal_code: Optional[str] = None) -> Optional[UserInDB]:
    user_collection = get_user_collection()
    
    address_update = {
        "address.latitude": latitude,
        "address.longitude": longitude,
        "updated_at": datetime.utcnow()
    }
    
    if street:
        address_update["address.street"] = street
    if city:
        address_update["address.city"] = city
    if state:
        address_update["address.state"] = state
    if country:
        address_update["address.country"] = country
    if postal_code:
        address_update["address.postal_code"] = postal_code
    
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": address_update}
    )
    
    return await get_user_by_id(user_id)