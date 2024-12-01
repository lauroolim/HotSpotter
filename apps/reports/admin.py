from django.contrib import admin
from django.contrib.gis.db import models
from mapwidgets.widgets import GoogleMapPointFieldWidget
from django.contrib import admin
from apps.reports.models import Report
import mapwidgets

class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'location', 'created_at', 'foto', 'user']
    search_fields = ['title']
    formfield_overrides = {
        models.PointField: {"widget": mapwidgets.GoogleMapPointFieldWidget}
    }

admin.site.register(Report, ReportAdmin)