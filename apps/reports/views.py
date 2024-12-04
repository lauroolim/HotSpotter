from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from .forms import ReportForm
from .models import Report
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from apps.reports.serializers import ReportSerializer
from rest_framework import permissions
import requests

class CreateReportView(LoginRequiredMixin, CreateView):
    template_name = "reports/report.html"
    form_class = ReportForm
    success_url = reverse_lazy('report-success')  

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.get_address(self.object) 
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "google_api_key": settings.GOOGLE_API_KEY,
        })
        return context
        
    def get_address(self, report):
        if report.location:
            lat = report.location.y
            lon = report.location.x
            google_api_key = settings.GOOGLE_API_KEY
            url = (
                f'https://maps.googleapis.com/maps/api/geocode/json'
                f'?latlng={lat},{lon}&key={google_api_key}&language=pt-BR'
            )
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                if data['results']:
                    report.address = data['results'][0]['formatted_address']
                    report.save(update_fields=['address'])

class ListReportsView(LoginRequiredMixin, ListView):
    model = Report
    context_object_name = 'reports'
    template_name = 'reports/list.html'

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/report-detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

class DeleteReportView(LoginRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('list-reports')

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

class ReportSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "reports/success.html"

class APIListReportsView(ListAPIView):
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.all()