from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardViewsTests(TestCase):
    def setUp(self):
        self.landing_url = reverse('dashboard:landing')
        self.home_url = reverse('dashboard:home')
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'SecurePassword123!'

    def test_landing_page_publicly_accessible(self):
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
        self.assertContains(response, 'Master Mocks with')

    def test_home_page_requires_login(self):
        response = self.client.get(self.home_url)
        # Should redirect to login page (accounts:login)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, f"{login_url}?next={self.home_url}")

    def test_home_page_accessible_to_logged_in_users(self):
        User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')
        self.assertContains(response, 'Hello, testuser!')
