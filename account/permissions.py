from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdmin(permissions.BasePermission):
    '''allows access to all users but gives special permissions to admin user'''


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:

            return True
        else:
            if request.user.is_staff and request.user.is_authenticated == True:
                return True

            return False


class IsUser(permissions.BasePermission):
    """This permission allows users to access the products of mrs favour
    """
    def has_permission(self,request, view):
        if request.method in permissions.SAFE_METHODS:

            return True
        else:
            if request.user.is_authenticated == True: 

                return True
            raise PermissionDenied(detail={
                "message": "User have not been Authenticated"
            })


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):

        if request.user:
            return True
        else:
            raise PermissionDenied(detail= {"message": "Permission denied"})
