from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from apps.reports.consts import *


class Report(models.Model):
    title = models.SmallIntegerField(choices=REPORTS_OPTIONS)
    description = models.TextField()
    location = gis_models.PointField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(blank=True, null=True, upload_to="static/images/reports")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_title_display()

