from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pengiriman.models import Pengiriman
from keranjang.models import Keranjang, ItemKeranjang
from pengiriman.forms import PengirimanForm
from main.models import Product
from decimal import Decimal


class PengirimanViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.product = Product.objects.create(
            nama_produk='Test Product',
            kategori='Dasi Instant',  
            harga=Decimal('100.00'),
            gambar_produk='http://example.com/image.png'  
        )
        self.keranjang = Keranjang.objects.create(user=self.user)
        self.item1 = ItemKeranjang.objects.create(keranjang=self.keranjang, product=self.product, quantity=2)
        self.item2 = ItemKeranjang.objects.create(keranjang=self.keranjang, product=self.product, quantity=3)
        self.keranjang_id = self.keranjang.id
        self.pengiriman_url = reverse('pengiriman:pengiriman') + f'?keranjang_id={self.keranjang_id}'
        self.process_pengiriman_ajax_url = reverse('pengiriman:process_pengiriman_ajax')
        self.show_json_url = reverse('pengiriman:show_json_pengiriman')

    def test_pengiriman_view_get(self):
        response = self.client.get(self.pengiriman_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pengiriman.html')
        self.assertIn('form', response.context)

    def test_pengiriman_view_post_valid_data(self):
        form_data = {
            'first_name': 'Deva',
            'last_name': 'Teuku',
            'email': 'Deva@example.com',
            'phone_number': 123456789,  
            'address': '123 Test St',
            'city': 'Jakarta Selatan', 
            'postal_code': 12345,       
            'courier': 'JNE'            
        }
        response = self.client.post(self.pengiriman_url, data=form_data)
        self.assertRedirects(response, reverse('pembayaran:pembayaran_view') + f'?keranjang_id={self.keranjang_id}')
        self.assertTrue(Pengiriman.objects.filter(user=self.user, first_name='Deva').exists())


    def test_pengiriman_view_post_invalid_data(self):
        incomplete_form_data = {
            'last_name': 'Teuku',
            'email': 'deva@example.com',
            'phone_number': 123456789,
            'city': 'Jakarta Selatan',
            'postal_code': 12345,
            'courier': 'JNE'
        }
        response = self.client.post(self.pengiriman_url, data=incomplete_form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('address', form.errors)

        

    def test_process_pengiriman_ajax_post_valid(self):
        self.assertTrue(self.keranjang.itemkeranjang_set.exists())

        valid_data = {
            'first_name': 'Deva',
            'last_name': 'Teuku',
            'email': 'deva.teuku@example.com',
            'phone_number': '1234567890',
            'address': '123 Main St',
            'city': 'Jakarta Barat',
            'postal_code': '12345',
            'courier': 'JNE',
        }

        response = self.client.post(
            self.process_pengiriman_ajax_url,
            data=valid_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('pengiriman_id', response.json()) 

    def test_process_pengiriman_ajax_empty_cart(self):
        self.keranjang.itemkeranjang_set.all().delete()
        form_data = {
            'first_name': 'Deva',
            'last_name': 'Teuku',
            'email': 'deva@example.com',
            'phone_number': '123456789',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'courier': 'Test Courier'
        }
        response = self.client.post(self.process_pengiriman_ajax_url, data=form_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Keranjang kosong, tidak dapat melakukan pengiriman.'})

    def test_process_pengiriman_ajax_invalid_request(self):
        form_data = {
            'first_name': 'Deva',
            'last_name': 'Teuku',
            'email': 'deva@example.com'
        }
        response = self.client.post(self.process_pengiriman_ajax_url, data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid request'})

    def test_show_json(self):
        Pengiriman.objects.create(
            user=self.user,
            first_name='Deva',
            last_name='Teuku',
            email='deva@example.com',
            phone_number=123456789,
            address='123 Test St',
            city='Jakarta Selatan',
            postal_code=12345,
            courier='JNE'
        )
        response = self.client.get(self.show_json_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('Deva', response.content.decode())

