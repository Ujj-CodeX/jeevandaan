# users/admin.py
from django.contrib import admin
from .models import Donor

# users/admin.py
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = ['name', 'blood_group', 'is_locked', 'is_aadhaar_verified', 'reliability_score', 'cancellation_count']
    list_filter = ['blood_group', 'is_locked', 'is_aadhaar_verified']
    search_fields = ['name', 'email', 'username']
    actions = ['lock_donor', 'unlock_donor', 'verify_aadhaar']

    
    def get_readonly_fields(self, request, obj=None):
        return [
            'name', 'email', 'username',
            'phone_number', 'address',
            'blood_group', 'password',
            'google_id', 'auth_provider',
            'aadhaar_number',
            'reliability_score',
            'total_donations',
            'cancellation_count',
            'created_at', 'updated_at'
        ]


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    
    def lock_donor(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        queryset.update(is_locked=True, locked_until=timezone.now() + timedelta(days=30))
    lock_donor.short_description = " Lock donor account"

    def unlock_donor(self, request, queryset):
        queryset.update(is_locked=False, locked_until=None)
    unlock_donor.short_description = " Unlock donor account"

    def verify_aadhaar(self, request, queryset):
        queryset.update(is_aadhaar_verified=True, verification_tag=True)
    verify_aadhaar.short_description = " Mark Aadhaar as verified"