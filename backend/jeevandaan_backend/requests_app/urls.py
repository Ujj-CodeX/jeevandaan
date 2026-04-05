from django.urls import path
from .views import (
    AttenderRequestCreateView,
    AttenderRequestListView,
    AttenderRequestDetailView,
    DonorPartnerRequestListView,
    PartnerDonorRequestCreateView,
    PartnerDonorRequestListView,
    DonorAcceptRequestView,
    DonorCancelRequestView,
    FulfillAttenderRequestView,
    GetRequestOTPView,
    VerifyOTPView,
    PartnerDonorRequestListDetailView,
    SubmitAttenderRatingView,
    SubmitDonorRatingView,  # ← new
    MyAttenderRequestsView,
)

urlpatterns = [
    # Attender requests
    path('attender/create/', AttenderRequestCreateView.as_view()),
    path('attender/list/', AttenderRequestListView.as_view()),
    path('attender/<uuid:reference_id>/', AttenderRequestDetailView.as_view()),

    # Partner donor requests
    path('donor/create/', PartnerDonorRequestCreateView.as_view()),
    path('donor/list/', PartnerDonorRequestListView.as_view()),
    path('donor/detail/', PartnerDonorRequestListDetailView.as_view()),
    path('donor/<int:request_id>/accept/', DonorAcceptRequestView.as_view()),
    path('donor/<int:request_id>/cancel/', DonorCancelRequestView.as_view()),
    path('attender/<uuid:reference_id>/fulfill/', FulfillAttenderRequestView.as_view()),
    path('otp/<int:request_id>/', GetRequestOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('donor-requests/', DonorPartnerRequestListView.as_view()),
    path('attender/<uuid:reference_id>/rate/', SubmitAttenderRatingView.as_view()),
    path('donor/<int:request_id>/rate/', SubmitDonorRatingView.as_view()),
    path('attender/my-requests/', MyAttenderRequestsView.as_view()),
]