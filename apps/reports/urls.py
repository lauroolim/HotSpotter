from django.urls import path, include
from .views import MapView

urlpatterns = [
    path("route/", MapView.as_view(), name="route"),
]
