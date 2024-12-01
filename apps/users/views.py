from rest_framework.views import APIView
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import UserSerializer
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views import View
from django.conf import settings
from django.contrib.auth import login

User = get_user_model()

class LoginView(APIView):
    success_url = reverse_lazy("report")

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return render(request, "auth/login.html")

    def post(self, request):
        email = request.POST.get('email') if request.POST else request.data.get('email')
        password = request.POST.get('password') if request.POST else request.data.get('password')
        
        user = get_object_or_404(User, email=email)
        if not user.check_password(password):
            if request.content_type == "application/json":
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            return render(request, "auth/login.html", {"message": "Invalid credentials"})

        login(request, user)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)

        if request.content_type == "application/json":
            return Response({"token": token.key, "user": serializer.data})

        return redirect(self.success_url)

class SignupView(APIView):
    success_url = reverse_lazy("login")

    def get(self, request):
        return render(request, "auth/signup.html")

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            token = Token.objects.create(user=user)

            if request.content_type == "application/json":
                return Response({"token": token.key, "user": serializer.data})
            
            return redirect(self.success_url) 
        
        if request.content_type == "application/json":
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, "auth/signup.html", {"errors": serializer.errors})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)