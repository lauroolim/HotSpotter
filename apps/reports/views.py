from django.views import View
from django.shortcuts import render
from django.conf import settings
from .mixins import Directions


class MapView(View):
    """View para exibir o mapa com todas as ocorrências"""

    template_name = "incidents/map.html"

    def get(self, request):
        # Obtém todas as ocorrências ativas
        reports = report.objects.filter(status__in=["pending", "in_progress"])

        context = {
            "google_api_key": settings.GOOGLE_API_KEY,
            "incidents": reports,
            # Centro inicial do mapa (pode ser configurado nas settings)
            "initial_lat": settings.MAP_DEFAULT_LAT,
            "initial_lng": settings.MAP_DEFAULT_LNG,
            "initial_zoom": settings.MAP_DEFAULT_ZOOM,
        }

        # Se foi solicitada uma ocorrência específica
        report_id = request.GET.get("report_id")
        if report_id:
            try:
                report = reports.get(id=report_id)
                context.update(
                    {
                        "selected_incident": report,
                        "center_lat": report.location.y,  # latitude
                        "center_lng": report.location.x,  # longitude
                    }
                )
            except report.DoesNotExist:
                messages.error(request, "Ocorrência não encontrada.")

        return render(request, self.template_name, context)


class ReportView(View):
    def get(self, request):
        return render(request, "reports/report.html")
