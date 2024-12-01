from django.urls import path, include
from .views import ReportView, ReportSuccessView, APIListReportsView

urlpatterns = [
    path('', ReportView.as_view(), name='report'),
    path('success/', ReportSuccessView.as_view(), name='report_success'),
    path('api/', APIListReportsView.as_view(), name='api_list_reports'),
] 
