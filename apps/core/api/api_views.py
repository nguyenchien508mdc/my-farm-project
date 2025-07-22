from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


from apps.core.schemas.user import UserSchema, UserCreateSchema, ChangePasswordSchema
from apps.core.mappers.user_mapper import user_to_schema
from apps.farm.mappers.farm_mapper import farm_to_schema

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

User = get_user_model()

# ✅ Danh sách user chưa thuộc farm
class FreeUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farm_id):
        users = User.objects.filter(is_active=True).exclude(farms__id=farm_id)
        return Response([user_to_schema(user).model_dump() for user in users])


# ✅ Danh sách toàn bộ user active
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(is_active=True)
        return Response([user_to_schema(user).model_dump() for user in users])


# ✅ API lấy thông tin cá nhân
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(user_to_schema(request.user).model_dump())

    def patch(self, request):
        for field, value in request.data.items():
            setattr(request.user, field, value)
        request.user.save()
        return Response(user_to_schema(request.user).model_dump())


# ✅ API đăng ký
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            schema = UserCreateSchema.model_validate(request.data)
            user = User.objects.create_user(
                username=schema.username,
                email=schema.email,
                password=schema.password,
                first_name=schema.first_name,
                last_name=schema.last_name
            )
            return Response(user_to_schema(user).model_dump(), status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# ✅ API đổi mật khẩu khi đăng nhập
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            schema = ChangePasswordSchema.model_validate(request.data)
            user = request.user

            if not user.check_password(schema.old_password):
                return Response({"old_password": ["Mật khẩu cũ không đúng."]}, status=400)

            if schema.new_password1 != schema.new_password2:
                return Response({"new_password2": ["Mật khẩu mới không khớp."]}, status=400)

            # Validate mật khẩu mới
            try:
                validate_password(schema.new_password1, user)
            except ValidationError as e:
                return Response({"new_password1": e.messages}, status=400)

            user.set_password(schema.new_password1)
            user.save()
            return Response({"detail": "Mật khẩu đã được thay đổi thành công."})

        except Exception as e:
            return Response({"error": str(e)}, status=400)

# ✅ API gửi email reset mật khẩu
class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Vui lòng nhập email."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Không tìm thấy người dùng với email này."}, status=400)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"http://localhost:8000/password-reset-confirm/{uid}/{token}/"

        send_mail(
            subject="Đặt lại mật khẩu",
            message=f"Nhấp vào liên kết để đặt lại mật khẩu: {reset_url}",
            from_email=None,
            recipient_list=[email],
        )
        return Response({"detail": "Email đặt lại mật khẩu đã được gửi."})


# ✅ API đặt lại mật khẩu (qua link)
class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')

        if not all([uidb64, token, password1, password2]):
            return Response({"detail": "Thiếu dữ liệu."}, status=400)

        if password1 != password2:
            return Response({"new_password2": ["Mật khẩu xác nhận không khớp."]}, status=400)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"uid": ["UID không hợp lệ."]}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"token": ["Token không hợp lệ hoặc đã hết hạn."]}, status=400)

        # Validate mật khẩu mới
        try:
            validate_password(password1, user)
        except ValidationError as e:
            return Response({"new_password1": e.messages}, status=400)

        user.set_password(password1)
        user.save()
        return Response({"detail": "Mật khẩu đã được thay đổi thành công."})

# ✅ API đăng nhập & lưu access/refresh token vào cookie
class CustomTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=30 * 60,
                path='/api/',
            )
            response.data.pop('access', None)

        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Strict',
                max_age=7 * 24 * 60 * 60,
                path='/',
            )
            response.data.pop('refresh', None)

        return super().finalize_response(request, response, *args, **kwargs)


# ✅ API refresh token từ cookie
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Không có refresh token'}, status=401)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Refresh token không hợp lệ hoặc hết hạn'}, status=403)

        return Response(serializer.validated_data)


# ✅ API logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({'detail': 'Đăng xuất thành công'})
    response.delete_cookie('access_token', path='/api/')
    response.delete_cookie('refresh_token', path='/')
    return response
