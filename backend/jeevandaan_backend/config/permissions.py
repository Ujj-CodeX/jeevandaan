from rest_framework.permissions import BasePermission


class IsDonor(BasePermission):
    message = 'Donor authentication required.'

    def has_permission(self, request, view):
        #  Simple check — no DB query
        if request.user is None:
            return False
        # Check if it's a donor by looking for donor-specific field
        return hasattr(request.user, 'blood_group')


class IsPartner(BasePermission):
    message = 'Partner authentication required.'

    def has_permission(self, request, view):
        if request.user is None:
            return False
        # Check if it's a partner by looking for partner-specific field
        return hasattr(request.user, 'hospital_name')


class IsAuthenticated(BasePermission):
    message = 'Authentication required.'

    def has_permission(self, request, view):
        return request.user is not None