from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users in the 'Admin' group.
    """
    def has_permission(self, request, view):
        # The user must be logged in AND in the 'Admin' group.
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

class IsDoctor(permissions.BasePermission):
    """
    Allows access only to users in the 'Doctor' group.
    """
    def has_permission(self, request, view):
        # The user must be logged in AND in the 'Doctor' group.
        return request.user.is_authenticated and request.user.groups.filter(name='Doctor').exists()

class IsLabTechnician(permissions.BasePermission):
    """
    Allows access only to users in the 'LabTechnician' group.
    """
    def has_permission(self, request, view):
        # The user must be logged in AND in the 'LabTechnician' group.
        return request.user.is_authenticated and request.user.groups.filter(name='Lab Technician').exists()

class IsReceptionist(permissions.BasePermission):
    """
    Allows access only to users in the 'Receptionist' group.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Receptionist').exists()

class IsPharmacist(permissions.BasePermission):
    """
    Allows access only to users in the 'Pharmacist' group.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Pharmacist').exists()