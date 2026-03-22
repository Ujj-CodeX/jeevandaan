from django.urls import path
from .views import SendMessageView, ChatHistoryView

urlpatterns = [
    path('<int:request_id>/send/', SendMessageView.as_view()),
    path('<int:request_id>/history/', ChatHistoryView.as_view()),
]