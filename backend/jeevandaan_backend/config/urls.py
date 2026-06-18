"""
URL configuration for jeevandaan_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from config.cron_views import (
    ExpireAttenderRequestsView,
    ExpireDonorRequestsView,
    UnlockDonorAccountsView,
    ExpireUnvisitedDonorRequestsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/stock/', include('stock.urls')),
    path('api/requests/', include('requests_app.urls')),
    path('api/donations/', include('donations.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('cron/expire-attender/', ExpireAttenderRequestsView.as_view()),
    path('cron/expire-donor/', ExpireDonorRequestsView.as_view()),
    path('cron/unlock-donors/', UnlockDonorAccountsView.as_view()),
    path('cron/expire-unvisited/', ExpireUnvisitedDonorRequestsView.as_view()),
    path('api/auth/', include('auth_token.urls')),

    
]
