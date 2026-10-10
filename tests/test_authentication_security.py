from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='secuser', password='Password123!')

    def test_private_pages_require_login(self):
        private_urls = [
            '/accounts/profile/',
            '/wallets/dashboard/',
            '/wallets/wallet/',
            '/wallets/transfer/',
            '/transactions/list/',
        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_authenticated_user_access_private_pages(self):
        self.client.login(username='secuser', password='Password123!')
        private_urls = [
            '/accounts/profile/',
            '/wallets/dashboard/',
            '/wallets/wallet/',
            '/wallets/transfer/',
            '/transactions/list/',
        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_public_pages_accessible(self):
        public_urls = [
            '/',
            '/accounts/login/',
            '/accounts/register/',
        ]
        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
