from django.urls import path

from .views import (
    access_user_collection,
    access_user_detail,
    change_password_and_login,
    current_user,
    exit_process_collection,
    forgot_password,
    login_with_password,
    logout_view,
    request_login_otp,
    sso_authorize,
    sso_token,
    verify_login_code,
)

urlpatterns = [
    path("me/", current_user, name="current-user"),
    path("access/users/", access_user_collection, name="access-user-collection"),
    path("access/users/<int:user_id>/", access_user_detail, name="access-user-detail"),
    path("access/exit-processes/", exit_process_collection, name="exit-process-collection"),
    path("auth/request-otp/", request_login_otp, name="request-login-otp"),
    path("auth/forgot-password/", forgot_password, name="forgot-password"),
    path("auth/verify-otp/", verify_login_code, name="verify-login-code"),
    path("auth/login/", login_with_password, name="login-with-password"),
    path("auth/change-password/", change_password_and_login, name="change-password-and-login"),
    path("auth/logout/", logout_view, name="logout-view"),
    path("auth/sso/authorize/", sso_authorize, name="sso-authorize"),
    path("auth/sso/token/", sso_token, name="sso-token"),
]
