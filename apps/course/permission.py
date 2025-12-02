from rest_framework.permissions import BasePermission

from apps.course.models import Course

class IsOwner(BasePermission):
    """Allows access only to the owner of the course"""

    def has_object_permission(self, request, view, obj: Course):
        return obj.owner == request.user
