from django.urls import path, include
from .views import CreateReportView, ReportSuccessView, APIListReportsView, DeleteReportView, ListReportsView, ReportDetailView

urlpatterns = [
    path('', CreateReportView.as_view(), name='report'),
    path('success/', ReportSuccessView.as_view(), name='report-success'),
    path('delete/<int:pk>/', DeleteReportView.as_view(), name='delete-report'),
    path('list/', ListReportsView.as_view(), name='list-reports'),
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('api/', APIListReportsView.as_view(), name='api-list-reports')
] 
