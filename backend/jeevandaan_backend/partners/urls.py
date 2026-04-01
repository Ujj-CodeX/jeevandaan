from django.urls import path
from .views import (
    PartnerRegisterView,
    PartnerLoginView,
    PartnerProfileView,
    PartnerPublicListView,
    NearbyPartnersView,      # ← add
    NearbyDonorsView ,
    UpdatePartnerLocationView,
    CreateCampView,              # ← new
    ScheduleAndNotifyCampView,   # ← new
    PartnerCampsView,            # ← new
    NearbyCampsView,             # ← new
    EnrollCampView,              # ← new
    UpdateStockAfterCampView,    # ← new
    CheckDashboardFreezeView, 
)

urlpatterns = [
    path('register/', PartnerRegisterView.as_view()),
    path('login/', PartnerLoginView.as_view()),
    path('profile/', PartnerProfileView.as_view()),
    path('list/', PartnerPublicListView.as_view()),
    path('nearby/', NearbyPartnersView.as_view()),           # ← add
    path('nearby-donors/', NearbyDonorsView.as_view()),
    path('update-location/', UpdatePartnerLocationView.as_view()),
    # Camp URLs
    path('camps/', PartnerCampsView.as_view()),
    path('camps/create/', CreateCampView.as_view()),
    path('camps/nearby/', NearbyCampsView.as_view()),
    path('camps/<int:camp_id>/notify/', ScheduleAndNotifyCampView.as_view()),
    path('camps/<int:camp_id>/enroll/', EnrollCampView.as_view()),
    path('camps/<int:camp_id>/update-stock/', UpdateStockAfterCampView.as_view()),
    path('camps/check-freeze/', CheckDashboardFreezeView.as_view()),
]