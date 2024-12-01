from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Report

User = get_user_model()

class ReportSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'description', 'location', 'created_at', 'foto', 'user']
        geo_field = 'location'