from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Report
from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class ReportSerializer(GeoFeatureModelSerializer):
    foto = Base64ImageField(required=False, represent_in_base64=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "description",
            "location",
            "created_at",
            "foto",
            "user",
        ]
        geo_field = "location"
    
    def get_title_display(self, obj):
        return obj.get_title_display()


    
