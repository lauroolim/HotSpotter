from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from apps.reports.models import Report

User = get_user_model()

class ReportViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.report = Report.objects.create(title=1, description="Teste", location=Point(1, 1), user=self.user)
        self.token = Token.objects.create(user=self.user)

    def test_report_detail_view_requires_login(self):
        report = Report.objects.create(title=1, description="Teste", location=Point(1, 1), user=self.user)
        response = self.client.get(reverse("report-detail", args=[report.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_create_report_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("report"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports/report.html")
        self.assertIn("google_api_key", response.context)   
        self.assertIn("form", response.context)

    def test_list_reports_view_requires_login(self):
        response = self.client.get(reverse("list-reports"))  
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_list_reports_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("list-reports"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports/list.html")

    def test_report_detail_view_requires_login(self):
        report = Report.objects.create(title=1, description="Teste", location=Point(1, 1), user=self.user)
        response = self.client.get(reverse("report-detail", args=[report.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_delete_report_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("delete-report", args=[self.report.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Report.objects.filter(id=self.report.id).exists())

    def test_api_list_reports_view_requires_authentication(self):
        response = self.client.get(reverse("api-list-reports"))  
        self.assertEqual(response.status_code, 401)
