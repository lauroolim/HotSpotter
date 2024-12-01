from django import forms
from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from mapwidgets.widgets import GoogleMapPointFieldWidget
from .models import Report
import mapwidgets
from .widgets import GoogleMapWidget

class ReportForm(forms.ModelForm):
    location = forms.CharField(widget=GoogleMapWidget)

    class Meta:
        model = Report
        fields = ['title', 'description', 'location', 'foto']

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location:
            try:
                lat, lng = map(float, location.split(','))
                return Point(lng, lat, srid=4326)
            except (ValueError, TypeError, AttributeError):
                raise forms.ValidationError('Invalid location format')
        return None
        
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'