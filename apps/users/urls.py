from django.urls import path
from .views import SignupView, LoginView, Logout

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', Logout.as_view(), name='logout'),
]
