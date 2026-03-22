from django.urls import path
from .views import (
    DonorNotificationListView,
    PartnerNotificationListView,
    MarkNotificationReadView,
    NotifyNearbyDonorsView
)

urlpatterns = [
    path('donor/', DonorNotificationListView.as_view()),
    path('partner/', PartnerNotificationListView.as_view()),
    path('<int:notification_id>/read/', MarkNotificationReadView.as_view()),
    path('notify-donors/', NotifyNearbyDonorsView.as_view()),
]