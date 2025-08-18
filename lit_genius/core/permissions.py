from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """
    Allows access only to users with the 'teacher' profile.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'teacher'
