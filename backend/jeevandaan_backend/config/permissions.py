from rest_framework.permissions import BasePermission


class IsDonor(BasePermission):
    """Only authenticated donors"""
    message = 'Donor authentication required.'

    def has_permission(self, request, view):
        return (
            request.user is not None and
            hasattr(request.user, 'blood_group')  
        )


class IsPartner(BasePermission):
    """Only authenticated partners"""
    message = 'Partner authentication required.'

    def has_permission(self, request, view):
        return (
            request.user is not None and
            hasattr(request.user, 'hospital_name')  
        )


class IsAuthenticated(BasePermission):
    """Any authenticated user — donor or partner"""
    message = 'Authentication required.'

    def has_permission(self, request, view):
        return request.user is not None