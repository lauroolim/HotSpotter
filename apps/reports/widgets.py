from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.conf import settings

class GoogleMapWidget(Input):
    class Media:
        css = {
            'all': ('css/map_widget.css',)
        }
        js = (
            f'https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_API_KEY}&libraries=places',
            'js/map_widget.js',
        )

    def render(self, name, value, attrs=None, **kwargs):
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'type': 'hidden',
            'class': 'map-coordinate-input',
            'readonly': 'readonly',
        })
        
        html = f"""
        <div class="map-widget-container">
            <input type="text" id="address_input" class="form-control mb-2" placeholder="Search location">
            <div id="map_canvas" style="height: 400px; margin-bottom: 10px;"></div>
            <button type="button" id="set_location" class="btn btn-primary mb-2">Definir Local</button>
            {super().render(name, value, attrs)}
        </div>
        """
        return mark_safe(html)