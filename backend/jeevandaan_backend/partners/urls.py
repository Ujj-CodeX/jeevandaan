from django.urls import path
from .views import (
    PartnerRegisterView,
    PartnerLoginView,
    PartnerProfileView,
    PartnerPublicListView,
    NearbyPartnersView,      # ← add
    NearbyDonorsView ,
)

urlpatterns = [
    path('register/', PartnerRegisterView.as_view()),
    path('login/', PartnerLoginView.as_view()),
    path('profile/', PartnerProfileView.as_view()),
    path('list/', PartnerPublicListView.as_view()),
    path('nearby/', NearbyPartnersView.as_view()),           # ← add
    path('nearby-donors/', NearbyDonorsView.as_view()),
]