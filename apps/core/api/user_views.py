from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from asgiref.sync import async_to_sync
import os
import time
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from rest_framework.parsers import MultiPartParser, FormParser

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.core.schemas.user_schema import (
    UserCreateSchema, ChangePasswordSchema, UserUpdateSchema
)
from apps.core.mappers.user_mapper import user_to_schema
from apps.core.services.user_service import UserService


user_service = UserService()


class FreeUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        try:
            users = async_to_sync(user_service.list_free_users)(farm_id)  # async -> sync
            return Response(users)  
        except Exception as e:
            import traceback; traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        users = async_to_sync(user_service.list_users)()
        return Response([user.model_dump() for user in users])

    def post(self, request):
        try:
            data = request.data.copy()
            if "profile_picture" in request.FILES:
                file = request.FILES["profile_picture"]
                username = data.get("username", None) or request.user.username or "user"
                base_filename = get_valid_filename(f"{username}_new")
                folder = "profile_pictures"
                if hasattr(file, "name") and hasattr(file, "read"):
                    # Xóa tất cả file có cùng tên base_filename bất kể đuôi gì
                    if default_storage.exists(folder):
                        # Lấy danh sách tất cả file trong thư mục
                        all_files = default_storage.listdir(folder)[1]  # [0] là folders, [1] là files
                        for existing_file in all_files:
                            if existing_file.startswith(base_filename):  # xóa tất cả file bắt đầu bằng "username_id"
                                file_path_to_delete = os.path.join(folder, existing_file)
                                if default_storage.exists(file_path_to_delete):
                                    default_storage.delete(file_path_to_delete)
                # Lưu file với timestamp để tránh cache
                ext = os.path.splitext(file.name)[1]
                filename = f"{base_filename}_{int(time.time())}{ext}"
                file_path = os.path.join(folder, filename)
                saved_path = default_storage.save(file_path, file)
                data["profile_picture"] = default_storage.url(saved_path)
            # Flatten dữ liệu
            flat_data = {
                k: v[0] if isinstance(v, (list, tuple)) and len(v) == 1 else v
                for k, v in data.items()
            }
            schema = UserCreateSchema.model_validate(flat_data)
            user = async_to_sync(user_service.create_user)(schema)
            return Response(user.model_dump(), status=201)
        except ValidationError as ve:
            return Response({"error": ve.errors()}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)


class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            success = async_to_sync(user_service.delete_user)(user_id)
            if success:
                return Response({"detail": "User đã được xóa thành công."})
            return Response({"detail": "User không tồn tại."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        try:
            data = request.data.copy()
            if "profile_picture" in request.FILES:
                file = request.FILES["profile_picture"]
                username = username = data.get("username", None) or request.user.username
                base_filename = get_valid_filename(f"{username}_{user_id}")
                # Thư mục lưu ảnh
                folder = "profile_pictures"
                # ✅ Chỉ xử lý nếu là file thật
                if hasattr(file, "name") and hasattr(file, "read"):
                    # Xóa tất cả file có cùng tên base_filename bất kể đuôi gì
                    if default_storage.exists(folder):
                        # Lấy danh sách tất cả file trong thư mục
                        all_files = default_storage.listdir(folder)[1]  # [0] là folders, [1] là files
                        for existing_file in all_files:
                            if existing_file.startswith(base_filename):  # xóa tất cả file bắt đầu bằng "username_id"
                                file_path_to_delete = os.path.join(folder, existing_file)
                                if default_storage.exists(file_path_to_delete):
                                    default_storage.delete(file_path_to_delete)
                # Lấy phần mở rộng file mới
                ext = os.path.splitext(file.name)[1]
                # Tạo tên file mới
                filename = f"{base_filename}_{int(time.time())}{ext}"
                file_path = os.path.join(folder, filename)
                # Lưu file mới
                saved_path = default_storage.save(file_path, file)
                data["profile_picture"] = default_storage.url(saved_path)
            # Flatten dữ liệu: convert list 1 phần tử thành giá trị đơn
            flat_data = {
                k: v[0] if isinstance(v, (list, tuple)) and len(v) == 1 else v
                for k, v in data.items()
            }
            schema = UserUpdateSchema.model_validate(flat_data)
            updated_user = async_to_sync(user_service.update_user)(user_id, schema)
            return Response(updated_user.model_dump())
        except ValidationError as e:
            return Response({"errors": e.errors()}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Chưa đăng nhập"}, status=401)
        
        user_schema = user_to_schema(request.user)
        return Response(user_schema.model_dump())


    def patch(self, request):
        try:
            schema = UserUpdateSchema.model_validate(request.data)
            updated_user = async_to_sync(user_service.update_user)(request.user.id, schema)
            return Response(updated_user.model_dump())
        except ValidationError as e:
            # e.message hoặc e.messages có thể là list hoặc string
            messages = e.messages if hasattr(e, 'messages') else [str(e)]
            return Response({"errors": messages}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            schema = UserCreateSchema.model_validate(request.data)
            user = async_to_sync(user_service.create_user)(schema)
            return Response(user.model_dump(), status=201)
        except ValidationError as ve:
            return Response({"error": ve.messages}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            schema = ChangePasswordSchema.model_validate(request.data)
            async_to_sync(user_service.change_password)(
                request.user.id,
                schema.old_password,
                schema.new_password1,
                schema.new_password2
            )
            return Response({"detail": "Mật khẩu đã được thay đổi thành công."})
        except ValidationError as ve:
            return Response({"error": ve.messages}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")
            if not email:
                return Response({"email": "Vui lòng nhập email."}, status=400)

            user = async_to_sync(user_service.get_by_email)(email)
            if not user:
                return Response({"detail": "Không tìm thấy người dùng với email này."}, status=400)

            reset_url = async_to_sync(user_service.generate_password_reset_link)(user, request)

            print(f"Password reset link: {reset_url}")

            return Response({"detail": "Email đặt lại mật khẩu đã được gửi (nội bộ/log)."})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"detail": str(e)}, status=500)



class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')

        if not all([token, password1, password2]):
            return Response({"detail": "Thiếu dữ liệu."}, status=400)

        if password1 != password2:
            return Response({"new_password2": ["Mật khẩu xác nhận không khớp."]}, status=400)

        try:
            validate_password(password1)
        except ValidationError as e:
            return Response({"new_password1": e.messages}, status=400)

        success = async_to_sync(user_service.confirm_password_reset)(token, password1)
        if not success:
            return Response({"token": ["Token không hợp lệ hoặc đã hết hạn."]}, status=400)

        return Response({"detail": "Mật khẩu đã được thay đổi thành công."})