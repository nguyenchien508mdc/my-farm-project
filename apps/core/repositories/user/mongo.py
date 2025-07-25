# apps/core/repositories/user/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from apps.core.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from typing import Optional, List, Union
from bson import ObjectId
from datetime import datetime
from passlib.hash import bcrypt
import uuid
import os


class MongoUserRepository:
    def __init__(self, db_url="mongodb://localhost:27017", db_name="mydb"):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["users"]

    def _format_user(self, user) -> dict:
        if not user:
            return None
        user["id"] = str(user["_id"])
        user["profile_picture"] = f"/media/{user.get('profile_picture', '')}" if user.get("profile_picture") else ""
        return user

    async def create_user(self, data: UserCreateSchema) -> dict:
        user_doc = {
            "username": data.username,
            "email": data.email,
            "password": bcrypt.hash(data.password),
            "first_name": data.first_name or "",
            "last_name": data.last_name or "",
            "phone_number": data.phone_number or "",
            "address": data.address or "",
            "date_of_birth": data.date_of_birth.isoformat() if data.date_of_birth else None,
            "is_verified": False,
            "role": "user",
            "profile_picture": None,
            "date_joined": datetime.utcnow().isoformat(),
            "is_active": True
        }
        result = await self.collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return self._format_user(user_doc)

    async def get_by_id(self, user_id: Union[str, ObjectId]) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return self._format_user(user)

    async def get_by_username(self, username: str) -> Optional[dict]:
        user = await self.collection.find_one({"username": username})
        return self._format_user(user)

    async def get_by_email(self, email: str) -> Optional[dict]:
        user = await self.collection.find_one({"email": email})
        return self._format_user(user)

    async def update_user(self, user_id: str, data: UserUpdateSchema) -> Optional[dict]:
        if not ObjectId.is_valid(user_id):
            return None
        ud = data.dict(exclude_unset=True)
        if "date_of_birth" in ud and isinstance(ud["date_of_birth"], datetime):
            ud["date_of_birth"] = ud["date_of_birth"].isoformat()

        if "profile_picture" in ud:
            pic = ud["profile_picture"]
            if hasattr(pic, "read") and hasattr(pic, "name"):
                ext = os.path.splitext(pic.name)[-1] or ".jpg"
                filename = f"{uuid.uuid4().hex}{ext}"
                filepath = os.path.join("media", "profile_pictures", filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(pic.read())
                ud["profile_picture"] = f"profile_pictures/{filename}"

        await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": ud})
        updated = await self.get_by_id(user_id)
        return updated

    async def delete_user(self, user_id: Union[str, ObjectId]) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

    async def change_password(self, user_id: str, new_password: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        new_hashed = bcrypt.hash(new_password)
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"password": new_hashed}}
        )
        return result.modified_count > 0

    async def get_password_hash(self, user_id: str) -> Optional[str]:
        if not ObjectId.is_valid(user_id):
            return None
        user = await self.collection.find_one({"_id": ObjectId(user_id)}, {"password": 1})
        return user["password"] if user else None

    async def list_users(self) -> List[dict]:
        users = []
        async for user in self.collection.find():
            users.append(self._format_user(user))
        return users

    async def list_free_users(self, farm_id: Union[str, ObjectId]) -> List[dict]:
        membership_col = self.db["farm_memberships"]
        used_user_ids = await membership_col.distinct("user_id", {"farm_id": farm_id})
        cursor = self.collection.find({"_id": {"$nin": used_user_ids}})
        return [self._format_user(u) async for u in cursor]

    async def initiate_password_reset(self, email: str) -> bool:
        user = await self.collection.find_one({"email": email})
        if not user:
            return False
        token = str(uuid.uuid4())
        expires_at = datetime.utcnow().timestamp() + 3600
        await self.db["reset_tokens"].insert_one({
            "user_id": user["_id"],
            "token": token,
            "expires_at": expires_at
        })
        print(f"Reset token for {email}: {token}")
        return True

    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        now_ts = datetime.utcnow().timestamp()
        token_doc = await self.db["reset_tokens"].find_one({"token": token, "expires_at": {"$gt": now_ts}})
        if not token_doc:
            return False
        user_id = token_doc["user_id"]
        new_hashed = bcrypt.hash(new_password)
        await self.collection.update_one({"_id": user_id}, {"$set": {"password": new_hashed}})
        await self.db["reset_tokens"].delete_one({"token": token})
        return True

    async def save_password_reset_token(self, user_id: str, token: str) -> None:
        await self.db["reset_tokens"].delete_many({"user_id": ObjectId(user_id)})
        expires_at = datetime.utcnow().timestamp() + 3600
        await self.db["reset_tokens"].insert_one({
            "user_id": ObjectId(user_id),
            "token": token,
            "expires_at": expires_at
        })

