from rest_framework.permissions import BasePermission
from .constants import Parent, Teacher, Admin


class IsAdminRole(BasePermission):
    message = "You don't have enough permission"

    def has_permission(self, request, view):
        if request.user:
            return request.user.role == Admin


class IsTeacherRole(BasePermission):
    message = "You don't have enough permission"

    def has_permission(self, request, view):
        if request.user:
            return request.user.role == Teacher


class IsAdminTeacherRole(BasePermission):
    message = "You don't have enough permission"

    def has_permission(self, request, view):
        if request.user:
            return request.user.role == Teacher or request.user.role == Admin
