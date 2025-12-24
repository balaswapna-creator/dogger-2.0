"""
Dogger 2.0 - Custom Permissions
"""
from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    """Allow only doctors"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'


class IsDoctorOrReceptionist(permissions.BasePermission):
    """Allow doctors and receptionists"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['doctor', 'receptionist']


class IsLabTech(permissions.BasePermission):
    """Allow lab technicians"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'lab_tech'


class CanAccessPatient(permissions.BasePermission):
    """Check if user can access specific patient"""
    def has_object_permission(self, request, view, obj):
        # Admin can access all
        if request.user.role == 'admin':
            return True
        
        # Safe methods allowed for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Doctors and receptionists can modify
        return request.user.role in ['doctor', 'receptionist']


class HasActiveSubscription(permissions.BasePermission):
    """Check if user has active subscription"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin always has access
        if request.user.is_staff:
            return True
        
        return request.user.is_active_subscription