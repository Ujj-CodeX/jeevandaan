# requests_app/admin.py
from django.contrib import admin
from .models import AttenderRequest, PartnerDonorRequest

@admin.register(AttenderRequest)
class AttenderRequestAdmin(admin.ModelAdmin):
    list_display = ['reference_id', 'patient_name', 'blood_group', 'quantity', 'urgency', 'status', 'created_at']
    list_filter = ['status', 'urgency', 'blood_group']
    search_fields = ['patient_name', 'hospital_name', 'reference_id']

@admin.register(PartnerDonorRequest)
class PartnerDonorRequestAdmin(admin.ModelAdmin):
    list_display = ['partner', 'blood_group', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'blood_group']