# partners/admin.py
from django.contrib import admin
from .models import Partners


# partners/admin.py
@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):

   
    list_display = ['hospital_name', 'license_id', 'city', 'is_verified', 'is_live']

    
    list_filter = ['is_verified', 'is_live', 'partner_type']

    
    search_fields = ['hospital_name', 'license_id']

    
    actions = ['verify_and_go_live', 'suspend_partner']

    
    def get_readonly_fields(self, request, obj=None):
        # These fields can NEVER be edited
        return [
            'hospital_name', 'email', 'contact',
            'address', 'city', 'state',
            'license_id', 'password',
            'convenience_fee', 'fee_description',
            'latitude', 'longitude',
            'created_at', 'updated_at'
        ]

    
    def has_add_permission(self, request):
        return False

    
    def has_delete_permission(self, request, obj=None):
        return False

    
    def verify_and_go_live(self, request, queryset):
        queryset.update(is_verified=True, is_live=True)
    verify_and_go_live.short_description = " Verify and activate partner"


    def suspend_partner(self, request, queryset):
        queryset.update(is_live=False)
    suspend_partner.short_description = " Suspend partner"