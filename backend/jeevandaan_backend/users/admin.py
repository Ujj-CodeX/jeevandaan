# users/admin.py
from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'blood_group', 'is_locked', 'is_aadhaar_verified', 'reliability_score']
    list_filter = ['blood_group', 'is_locked', 'is_aadhaar_verified', 'auth_provider']
    search_fields = ['name', 'email', 'username']
    actions = ['lock_donors', 'unlock_donors']

    def lock_donors(self, request, queryset):
        queryset.update(is_locked=True)
    lock_donors.short_description = "Lock selected donors"

    def unlock_donors(self, request, queryset):
        queryset.update(is_locked=False)
    unlock_donors.short_description = "Unlock selected donors"