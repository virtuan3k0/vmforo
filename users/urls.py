from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserDetailView, UserProfileUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('me/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
]