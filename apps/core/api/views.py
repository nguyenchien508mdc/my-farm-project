# apps/core/api_views.py

from rest_framework import generics, permissions
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserCreateSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from rest_framework import status
from django.core.mail import send_mail
User = get_user_model()

# ✅API lấy danh sách user chưa thuộc farm
class FreeUsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, farm_id):
        # Lấy tất cả user active
        users = User.objects.filter(is_active=True)

        # Lọc bỏ user đã thuộc farm
        users_free = users.exclude(farms__id=farm_id)

        serializer = UserSerializer(users_free, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# ✅API lấy danh sách tất cả user active
class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
# ✅ API đăng ký
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

# ✅ API lấy thông tin người dùng
class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)  # partial=True cho phép cập nhật 1 phần
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ API đổi mật khẩu
class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'detail': 'Mật khẩu đã được thay đổi thành công.'})

# ✅ API gửi mail đổi mật khẩu
class PasswordResetAPIView(APIView):
    permission_classes = [permissions.AllowAny]

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

        # Gửi email (hoặc log ra console nếu đang dev)
        send_mail(
            subject="Đặt lại mật khẩu",
            message=f"Nhấp vào liên kết để đặt lại mật khẩu: {reset_url}",
            from_email=None,
            recipient_list=[email],
        )

        return Response({"detail": "Email đặt lại mật khẩu đã được gửi."}, status=200)

def validate_complex_password(password):
    import re
    errors = []
    if len(password) < 8:
        errors.append("Mật khẩu phải có ít nhất 8 ký tự.")
    if not re.search(r'[A-Z]', password):
        errors.append("Mật khẩu phải chứa ít nhất 1 chữ hoa.")
    if not re.search(r'[a-z]', password):
        errors.append("Mật khẩu phải chứa ít nhất 1 chữ thường.")
    if not re.search(r'\d', password):
        errors.append("Mật khẩu phải chứa ít nhất 1 số.")
    if not re.search(r'[^A-Za-z0-9]', password):
        errors.append("Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt.")
    return errors


# ✅ API đặt lại mật khẩu nhận qua mail
class PasswordResetConfirmAPIView(APIView):
    permission_classes = []

    def post(self, request):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import default_token_generator
        from django.contrib.auth import get_user_model
        User = get_user_model()

        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')

        if not all([uidb64, token, password1, password2]):
            return Response({"detail": "Thiếu dữ liệu."}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response({"new_password2": ["Mật khẩu xác nhận không khớp."]}, status=status.HTTP_400_BAD_REQUEST)

        errors = validate_complex_password(password1)
        if errors:
            return Response({"new_password1": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"uid": ["UID không hợp lệ."]}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"token": ["Token không hợp lệ hoặc đã hết hạn."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password1)
        user.save()

        return Response({"detail": "Mật khẩu đã được thay đổi thành công."})
    
# ✅ API đặt lại mật khẩu user đăng nhập 
class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        if not old_password or not new_password1 or not new_password2:
            return Response({"detail": "Vui lòng điền đầy đủ thông tin."}, status=400)

        if not user.check_password(old_password):
            return Response({"old_password": ["Mật khẩu cũ không đúng."]}, status=400)

        if new_password1 != new_password2:
            return Response({"new_password2": ["Mật khẩu mới không khớp."]}, status=400)

        errors = validate_complex_password(new_password1)
        if errors:
            return Response({"new_password1": errors}, status=400)

        user.set_password(new_password1)
        user.save()
        return Response({"detail": "Mật khẩu đã được thay đổi thành công."})

# ✅ API đăng nhập & set access + refresh token vào cookie
class CustomTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')

        # Set access token cookie
        if access_token:
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=30 * 60,  
                path='/api/',     # cho tất cả các API
            )
            response.data.pop('access', None)  # Ẩn khỏi frontend

        # Set refresh token cookie
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

# ✅ API lấy refresh token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Lấy refresh token từ cookie HttpOnly thay vì body
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Không có refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Refresh token không hợp lệ hoặc hết hạn'}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.validated_data)

# ✅ Đăng xuất
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({'detail': 'Đăng xuất thành công'})
    response.delete_cookie('access_token', path='/api/')
    response.delete_cookie('refresh_token', path='/')
    return response

