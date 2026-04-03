# requests_app/admin.py
from django.contrib import admin
from .models import AttenderRequest, PartnerDonorRequest

# requests_app/admin.py
@admin.register(AttenderRequest)
class AttenderRequestAdmin(admin.ModelAdmin):

    list_display = ['reference_id', 'patient_name', 'blood_group', 'urgency', 'status', 'hospital_name', 'created_at']
    list_filter = ['status', 'urgency', 'blood_group']
    search_fields = ['patient_name', 'hospital_name', 'reference_id']
    actions = ['cancel_request']

    
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    #  Only cancel suspicious requests
    def cancel_request(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_request.short_description = " Cancel suspicious request"


@admin.register(PartnerDonorRequest)
class PartnerDonorRequestAdmin(admin.ModelAdmin):

    list_display = ['partner', 'blood_group', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'blood_group']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False