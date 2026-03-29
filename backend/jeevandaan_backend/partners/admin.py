# partners/admin.py
from django.contrib import admin
from .models import Partners

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ['hospital_name', 'license_id', 'city', 'is_verified', 'is_live', 'partner_type']
    list_filter = ['is_verified', 'is_live', 'partner_type', 'city']
    search_fields = ['hospital_name', 'license_id', 'email']
    actions = ['verify_partners', 'go_live']

    def verify_partners(self, request, queryset):
        queryset.update(is_verified=True)
    verify_partners.short_description = "Mark as verified"

    def go_live(self, request, queryset):
        queryset.update(is_live=True, is_verified=True)
    go_live.short_description = "Verify and go live"