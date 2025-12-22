from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to everyone, but write access only to admins.
    This is perfect for blog endpoints where:
    - Anyone can view blogs (GET)
    - Only admins can create, update, or delete blogs (POST, PUT, DELETE)
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin users
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'admin'
        )


class IsVerifiedUser(permissions.BasePermission):
    """
    Allows access only to verified users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_verified
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    Assumes the model instance has an `owner` or `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin users can do anything
        if request.user.user_type == 'admin':
            return True
        
        # Check if object has owner attribute
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Check if object has user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False
