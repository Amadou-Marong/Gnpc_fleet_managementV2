from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListCreateView, 
    UserRetrieveUpdateDestroyView,
    UserFormOptionsView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('auth/user-options', UserFormOptionsView.as_view(), name='user-form-options'),
    path('auth/users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
]