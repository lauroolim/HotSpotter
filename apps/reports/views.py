from django.views.generic.edit import CreateView 
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from .forms import ReportForm
from .models import Report
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from apps.reports.serializers import ReportSerializer
from rest_framework import permissions

class ReportView(LoginRequiredMixin, CreateView):
    template_name = "reports/report.html"
    form_class = ReportForm
    success_url = reverse_lazy('report_success')  

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "google_api_key": settings.GOOGLE_API_KEY,
        })
        return context

class ReportSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "reports/success.html"

class APIListReportsView(ListAPIView):
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.all()