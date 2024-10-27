from django.test import TestCase
from .models import Ulasan
from django.contrib.auth.models import User

class UlasanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_ulasan(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/your_app/create/', {
            'product_name': 'Test Product',
            'rating': 5,
            'likes': 0,
            'dislikes': 0
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Ulasan.objects.filter(user=self.user, product_name='Test Product').exists())

    def test_delete_ulasan(self):
        ulasan = Ulasan.objects.create(user=self.user, product_name='Test Product', rating=5)
        response = self.client.post(f'/your_app/hapus/{ulasan.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ulasan.objects.filter(pk=ulasan.pk).exists())

    def test_show_json(self):
        response = self.client.get('/your_app/show/')
        self.assertEqual(response.status_code, 200)

    def test_show_json_ajax(self):
        response = self.client.get('/your_app/show/ajax/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)