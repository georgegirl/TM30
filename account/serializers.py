from rest_framework import serializers



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class LogoutSerializer(serializers.Serializer):
    refresh_token= serializers.CharField()

