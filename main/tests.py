from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Product

class mainTest(TestCase):
    def test_login_page_accessible(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
