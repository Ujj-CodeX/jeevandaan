# donations/admin.py
from django.contrib import admin
from .models import DonationHistory

# donations/admin.py
@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):

    list_display = ['donor', 'partner', 'blood_group', 'units_donated', 'status', 'is_verified_by_bank', 'donated_at']
    list_filter = ['status', 'blood_group', 'is_verified_by_bank']

   
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False  # ← Cannot even open edit form!