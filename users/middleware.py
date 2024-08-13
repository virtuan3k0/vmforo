# users/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            return  # User is already authenticated

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]
            jwt_auth = JWTAuthentication()

            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                if isinstance(user, User):
                    login(request, user)  # Establish Django session
            except Exception as e:
                request.user = AnonymousUser()  # Fallback to anonymous if token invalid

