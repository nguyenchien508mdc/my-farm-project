# apps/core/repositories/user/base.py

from abc import ABC, abstractmethod
from typing import Optional, List, Union
from apps.core.schemas.user_schema import UserCreateSchema, UserUpdateSchema

class AbstractUserRepository(ABC):

    @abstractmethod
    async def create_user(self, data: UserCreateSchema) -> dict:
        """Tạo user (dùng cho đăng ký)"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: Union[str, int]) -> Optional[dict]:
        pass

    @abstractmethod
    async def update_user(self, user_id: Union[str, int], data: UserUpdateSchema) -> dict:
        """Cập nhật thông tin user (email, first_name, last_name, ...)"""
        pass

    @abstractmethod
    async def delete_user(self, user_id: Union[str, int]) -> bool:
        """Xoá user (mặc định xoá mềm nếu hỗ trợ)"""
        pass

    @abstractmethod
    async def change_password(self, user_id: Union[str, int], new_password: str) -> bool:
        """Thay đổi mật khẩu"""
        pass

    @abstractmethod
    async def initiate_password_reset(self, email: str) -> bool:
        """Bắt đầu quy trình đặt lại mật khẩu (gửi email hoặc tạo mã)"""
        pass

    @abstractmethod
    async def confirm_password_reset(self, token: str, new_password: str) -> bool:
        """Xác nhận token và đặt lại mật khẩu"""
        pass

    @abstractmethod
    async def list_users(self) -> List[dict]:
        """Lấy danh sách user (admin hoặc farm manager dùng)"""
        pass

    @abstractmethod
    async def list_free_users(self, farm_id: Union[str, int]) -> List[dict]:
        """Lấy danh sách user chưa gán farm (hoặc được lọc theo farm)"""
        pass

