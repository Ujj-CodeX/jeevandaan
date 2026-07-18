from django.urls import path
from .views import (
    StockUpdateView,
    PartnerStockView,
    StockSearchView
)

urlpatterns = [
    path('update/', StockUpdateView.as_view()),
    path('partner/<int:partner_id>/', PartnerStockView.as_view()),
    path('search/', StockSearchView.as_view()),
]