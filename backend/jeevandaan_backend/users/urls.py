from django.urls import path
from .views import DonorRegisterView, DonorLoginView, DonorProfileView

urlpatterns = [
    path('register/', DonorRegisterView.as_view()),
    path('login/', DonorLoginView.as_view()),
    path('profile/', DonorProfileView.as_view()),
]