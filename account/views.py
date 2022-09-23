from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import LogoutSerializer, LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.signals import user_logged_in, user_logged_out 
from .permissions import IsAdmin, IsAuthenticated, IsAuthenticated



@swagger_auto_schema(method="post",request_body=LoginSerializer()) 
@api_view(["POST"])
def login_view(request):

    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username = serializer.validated_data['username'], password= serializer.validated_data['password'])
        if user:
            if user.is_active:
                try:
                    refresh = RefreshToken.for_user(user)

                    user_details = {}
                    user_details['id'] = user.id
                    user_details['username'] = user.username
                    user_details['email'] = user.email
                    user_details['refresh-token'] = str(refresh)
                    user_details['access_token'] = str(refresh.access_token)
                    user_logged_in.send(sender= user.__class__,
                                        request=request, user=user)

                    data ={
                        "message": "success",
                        "data": user_details,
                    }
                    return Response(data, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                data= {
                    "message": "failed",
                    "errors": 'This account is not active'
                }
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            data= {
                "message": "failed",
                "errors": 'Please provide a valid username and password'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method="post", request_body=LogoutSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """"""

    
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid()

    try:
        token = RefreshToken(token=serializer.validated_data["refresh_token"])
        token.blacklist()
        user=request.user
        user_logged_out.send(sender=user.__class__,
                                        request=request, user=user)
        logout(request)
        return Response({"message": "success"}, status=status.HTTP_202_ACCEPTED)
    except TokenError:
        return Response({"message": "failed", "error": "invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
