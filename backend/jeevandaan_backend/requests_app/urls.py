from django.urls import path
from .views import (
    AttenderRequestCreateView,
    AttenderRequestListView,
    AttenderRequestDetailView,
    PartnerDonorRequestCreateView,
    PartnerDonorRequestListView,
    DonorAcceptRequestView,
    DonorCancelRequestView
)

urlpatterns = [
    # Attender requests
    path('attender/create/', AttenderRequestCreateView.as_view()),
    path('attender/list/', AttenderRequestListView.as_view()),
    path('attender/<uuid:reference_id>/', AttenderRequestDetailView.as_view()),

    # Partner donor requests
    path('donor/create/', PartnerDonorRequestCreateView.as_view()),
    path('donor/list/', PartnerDonorRequestListView.as_view()),
    path('donor/<int:request_id>/accept/', DonorAcceptRequestView.as_view()),
    path('donor/<int:request_id>/cancel/', DonorCancelRequestView.as_view()),
]