from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Product
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class mainTest(TestCase):
    def test_login_page_accessible(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
    
    # Test ini akan menguji registrasi yang berhasil dan gagal.
    def test_registration_success(self):
        response = self.client.post(reverse('main:register'), {
            'username': 'dummy1',
            'password1': 'HID1,Ijadft.',
            'password2': 'HID1,Ijadft.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='dummy1').exists())

    def test_registration_failure(self):
        response = self.client.post(reverse('main:register'), {
            'username': 'dummy2',
            'password1': 'HID2,Iltfit.',
            'password2': 'IforgotMyPass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='dummy2').exists())

    # Test ini akan membuat suate user baru dengan nama dummy1 dan coba login dengan password benar.
    # Selain itu, test ini akan menguji kasus ketika username salah dan kasus ketika password salah.
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='dummy1',
            password='HID1,Ijadft.',
        )

    def test_login_success(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'dummy1',
            'password': 'HID1,Ijadft.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_failure_username(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'dummy2',
            'password': 'HID1,Ijadft.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_failure_password(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'dummy1',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)