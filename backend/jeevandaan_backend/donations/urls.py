from django.urls import path
from .views import (
    VerifyDonationView,
    DonorHistoryView,
    PartnerDonationHistoryView,
    DonorLeaderboardView
)

urlpatterns = [
    path('verify/<int:request_id>/', VerifyDonationView.as_view()),
    path('my-history/', DonorHistoryView.as_view()),
    path('partner-history/', PartnerDonationHistoryView.as_view()),  # ← add
    path('leaderboard/', DonorLeaderboardView.as_view()),
]  