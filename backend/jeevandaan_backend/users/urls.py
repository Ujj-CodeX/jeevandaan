from django.urls import path
from .views import DonorRegisterView, DonorLoginView, DonorProfileView,UpdateDonorLocationView,ForgotPasswordView, ResetPasswordView, ChangePasswordView, VerifyAadhaarView, UpdateProfileView, ExpireAttenderRequestsView, ExpireDonorRequestsView, UnlockDonorAccountsView, ExpireUnvisitedDonorRequestsView

urlpatterns = [
    path('register/', DonorRegisterView.as_view()),
    path('login/', DonorLoginView.as_view()),
    path('profile/', DonorProfileView.as_view()),
    path('update-location/', UpdateDonorLocationView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('verify-aadhaar/', VerifyAadhaarView.as_view()),
    path('update-profile/', UpdateProfileView.as_view()),
    path('cron/expire-attender/', ExpireAttenderRequestsView.as_view()),
    path('cron/expire-donor/', ExpireDonorRequestsView.as_view()),
    path('cron/unlock-donors/', UnlockDonorAccountsView.as_view()),
    path('cron/expire-unvisited/', ExpireUnvisitedDonorRequestsView.as_view()),

]