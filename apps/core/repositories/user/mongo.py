# apps/core/repositories/user/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from apps.core.schemas.user_schema import UserCreateSchema
from typing import Optional

class MongoUserRepository:
    def __init__(self, db_url="mongodb://localhost:27017", db_name="mydb"):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["users"]

    async def create_user(self, data: UserCreateSchema) -> dict:
        # Chuẩn bị document
        user_doc = {
            "username": data.username,
            "email": data.email,
            "password": data.password,  # Bạn nên hash trước khi lưu
            "first_name": data.first_name or "",
            "last_name": data.last_name or "",
            # Có thể thêm các trường mặc định khác
        }
        result = await self.collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc

    async def get_by_username(self, username: str) -> Optional[dict]:
        return await self.collection.find_one({"username": username})

    async def get_by_email(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email})

    async def get_by_id(self, user_id) -> Optional[dict]:
        from bson import ObjectId
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})
