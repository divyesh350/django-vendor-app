from django.urls import path
from .views import SendOTPView, VerifyOTPView, SignupView, GetProfileView

app_name = 'vendor'

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', GetProfileView.as_view(), name='profile'),
] 