from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterAPI.as_view(), name="register"),
    path("userinfo/", views.UserAPI.as_view(), name="user_info"),
    path("resendotp/", views.ResendOtpAPI.as_view()),
    path("verify/", views.VerifyOTP.as_view()),
]
