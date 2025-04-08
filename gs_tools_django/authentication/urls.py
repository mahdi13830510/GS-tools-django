from django.urls import path

from gs_tools_django.authentication.views import SMSLoginRequestView, TokenObtainPairView, AuthenticationView

app_name = "authentication"

urlpatterns = [
    path("sms-otp/", SMSLoginRequestView.as_view(), name="sms_login"),
    path("otp-verify/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("login/", AuthenticationView.as_view(), name="login"),
]