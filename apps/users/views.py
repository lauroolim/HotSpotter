from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.shortcuts import render

from .serializers import UserSerializer


class LoginView(APIView):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        print(request.data)
        user = get_object_or_404(User, email=request.data["email"])
        if not user.check_password(request.data["password"]):
            return Response({"detail": "Not found"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        return Response({"token": token.key, "user": serializer.data})


class SignupView(APIView):
    def get(self, request):
        return render(request, "auth/signup.html")

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
