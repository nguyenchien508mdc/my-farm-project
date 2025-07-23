from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

# API đăng nhập & lưu access/refresh token vào cookie
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

# API refresh token từ cookie
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

# API logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({'detail': 'Đăng xuất thành công'})
    response.delete_cookie('access_token', path='/api/')
    response.delete_cookie('refresh_token', path='/')
    return response
