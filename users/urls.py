from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from users.apps import UsersConfig
from users.views import RegisterAPIView, VerifyEmailAPIView

app_name = UsersConfig.name  # Задаем имя для этого приложения

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterAPIView.as_view(), name="api_register"),
    path("verify/", VerifyEmailAPIView.as_view(), name="api_verify"),
]
