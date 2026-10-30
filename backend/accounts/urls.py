from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (RegisterAPIView,LoginAPIView,MyProfileAPIView,PublicUserProfileAPIView,LogoutAPIView,)

urlpatterns=[
    path("register/",RegisterAPIView.as_view(),name='register'),
    path("login/",LoginAPIView.as_view(),name='login'),
    path("token/refresh/",TokenRefreshView.as_view(),name='token_refresh'),
    path("me/",MyProfileAPIView.as_view(),name='my_profile'),
    path("logout/",LogoutAPIView.as_view(),name='logout'),
    path("users/<str:username>/",PublicUserProfileAPIView.as_view(),name='public_user_profile'),
]