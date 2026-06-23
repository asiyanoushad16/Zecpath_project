

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "employer"


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "candidate"