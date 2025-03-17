from rest_framework import permissions
from django.contrib.auth.models import Permission
from .models import User

class IsAdminOrHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role and request.user.role.name in ['Admin']

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role and request.user.role.name == 'Admin'

class IsHRUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role and request.user.role.name == 'User'

def has_permission(user_email, codename):
    """
    Check if a user has the necessary permission based on their role.
    """
    try:
        user = User.objects.get(email=user_email)
        if user.role and (user.role.name == 'Admin' or user.role.permissions.filter(codename=codename).exists()):
            return True
    except User.DoesNotExist:
        pass  # If the user doesn't exist, return False
    return False

class UserPermissions(permissions.BasePermission):
    """
    Custom permission class that determines permission codenames based on HTTP method and model name.
    """

    def has_permission(user_email, codename):
        """
        Check if a user has the necessary permission based on their role.
        """
        try:
            user = User.objects.get(email=user_email)
            print(f"Checking permissions for user: {user.email}, role: {user.role.name}")

            if user.role and user.role.name == 'Admin':
                print(f"✅ {user.email} is an Admin (Full Access)")
                return True

            role_permissions = user.role.permissions.all()
            print(f"🔹 Available permissions for role {user.role.name}: {[perm.codename for perm in role_permissions]}")

            if user.role and user.role.permissions.filter(codename=codename).exists():
                print(f"✅ Permission '{codename}' found for user {user.email}")
                return True

        except User.DoesNotExist:
            print("❌ User not found")
            return False
        except AttributeError as e:
            print(f"❌ AttributeError: {e} (Check if user.role exists)")
            return False

        print(f"❌ Permission '{codename}' NOT found for user {user_email}")
        return False
