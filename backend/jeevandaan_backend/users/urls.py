from django.urls import path
from .views import DonorRegisterView, DonorLoginView, DonorProfileView,GoogleAuthView

urlpatterns = [
    path('register/', DonorRegisterView.as_view()),
    path('login/', DonorLoginView.as_view()),
    path('profile/', DonorProfileView.as_view()),
    path('google/', GoogleAuthView.as_view()),

]