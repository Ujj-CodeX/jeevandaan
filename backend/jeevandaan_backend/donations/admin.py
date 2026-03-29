# donations/admin.py
from django.contrib import admin
from .models import DonationHistory

@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ['donor', 'partner', 'blood_group', 'units_donated', 'status', 'is_verified_by_bank', 'donated_at']
    list_filter = ['status', 'blood_group', 'is_verified_by_bank']