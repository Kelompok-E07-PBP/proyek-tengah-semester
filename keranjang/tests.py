from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from decimal import Decimal
from .models import Keranjang, ItemKeranjang
from .forms import TambahKeKeranjangForm, UpdateItemKeranjangForm
from main.models import Product
import uuid
import json

User = get_user_model()

class KeranjangModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.keranjang = Keranjang.objects.create(user=self.user)
        self.product1 = Product.objects.create(
            id=uuid.uuid4(),
            nama_produk='Test Product 1',
            harga=10000
        )
        self.product2 = Product.objects.create(
            id=uuid.uuid4(),
            nama_produk='Test Product 2',
            harga=15000
        )

    def test_keranjang_creation(self):
        """Test Keranjang model creation and string representation"""
        self.assertTrue(isinstance(self.keranjang, Keranjang))
        self.assertEqual(str(self.keranjang), f"Keranjang - {self.user.username}")

    def test_get_total_empty_cart(self):
        """Test get_total method with empty cart"""
        self.assertEqual(self.keranjang.get_total(), 0)

    def test_get_total_with_items(self):
        """Test get_total method with multiple items"""
        ItemKeranjang.objects.create(
            keranjang=self.keranjang,
            product=self.product1,
            quantity=2
        )
        ItemKeranjang.objects.create(
            keranjang=self.keranjang,
            product=self.product2,
            quantity=1
        )
        expected_total = (2 * self.product1.harga) + self.product2.harga
        self.assertEqual(self.keranjang.get_total(), expected_total)

class ItemKeranjangModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.keranjang = Keranjang.objects.create(user=self.user)
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            nama_produk='Test Product',
            harga=10000
        )
        self.item = ItemKeranjang.objects.create(
            keranjang=self.keranjang,
            product=self.product,
            quantity=2
        )

    def test_item_keranjang_creation(self):
        """Test ItemKeranjang model creation and string representation"""
        self.assertTrue(isinstance(self.item, ItemKeranjang))
        self.assertEqual(
            str(self.item),
            f"{self.product.nama_produk} (2)"
        )

    def test_get_subtotal(self):
        """Test get_subtotal calculation"""
        expected_subtotal = self.product.harga * 2
        self.assertEqual(self.item.get_subtotal(), expected_subtotal)

    def test_cascade_delete(self):
        """Test that ItemKeranjang is deleted when Keranjang is deleted"""
        item_id = self.item.id
        self.keranjang.delete()
        self.assertFalse(ItemKeranjang.objects.filter(id=item_id).exists())

class KeranjangFormTest(TestCase):
    def test_tambah_ke_keranjang_form_valid(self):
        """Test TambahKeKeranjangForm with valid data"""
        form = TambahKeKeranjangForm(data={'quantity': 1})
        self.assertTrue(form.is_valid())

    def test_tambah_ke_keranjang_form_invalid(self):
        """Test TambahKeKeranjangForm with invalid data"""
        form = TambahKeKeranjangForm(data={'quantity': 0})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['quantity'][0], "Ensure this value is greater than or equal to 1.")

        form = TambahKeKeranjangForm(data={'quantity': -1})
        self.assertFalse(form.is_valid())

        form = TambahKeKeranjangForm(data={'quantity': 'abc'})
        self.assertFalse(form.is_valid())

    def test_update_item_keranjang_form_valid(self):
        """Test UpdateItemKeranjangForm with valid data"""
        form = UpdateItemKeranjangForm(data={'quantity': 5})
        self.assertTrue(form.is_valid())

    def test_update_item_keranjang_form_invalid(self):
        """Test UpdateItemKeranjangForm with invalid data"""
        form = UpdateItemKeranjangForm(data={'quantity': 0})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['quantity'][0], "Jumlah minimal adalah 1")

        form = UpdateItemKeranjangForm(data={'quantity': -1})
        self.assertFalse(form.is_valid())

class KeranjangViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            nama_produk='Test Product',
            harga=10000
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.keranjang = Keranjang.objects.create(user=self.user)
        self.item = ItemKeranjang.objects.create(
            keranjang=self.keranjang,
            product=self.product,
            quantity=1
        )

    def test_keranjang_detail_view(self):
        """Test the shopping cart detail view"""
        response = self.client.get(reverse('keranjang_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'keranjang_detail.html')
        self.assertContains(response, self.product.nama_produk)

    def test_keranjang_detail_view_unauthenticated(self):
        """Test that unauthenticated users are redirected to login"""
        self.client.logout()
        response = self.client.get(reverse('keranjang_detail'))
        expected_url = '/login?next=/keranjang/keranjang/'
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200, fetch_redirect_response=False)

    def test_tambah_ke_keranjang_get_request(self):
        """Test GET request to add to cart view"""
        response = self.client.get(
            reverse('tambah_ke_keranjang', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tambah_ke_keranjang.html')

    def test_tambah_ke_keranjang_post_request(self):
        """Test POST request to add to cart"""
        response = self.client.post(
            reverse('tambah_ke_keranjang', args=[self.product.id]),
            {'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            ItemKeranjang.objects.get(product=self.product).quantity,
            3  # 1 from setUp + 2 from this test
        )

    def test_tambah_ke_keranjang_ajax_invalid_uuid(self):
        """Test adding item with invalid UUID via AJAX"""
        response = self.client.post(
            reverse('tambah_ke_keranjang_ajax', args=['not-a-uuid']),
            {'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_update_keranjang_invalid_quantity(self):
        """Test updating cart with invalid quantity"""
        response = self.client.post(
            reverse('update_keranjang', args=[self.item.id]),
            {'quantity': 'invalid'}
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Jumlah tidak valid', str(messages[0]))

    def test_update_keranjang_zero_quantity(self):
        """Test updating cart with zero quantity"""
        response = self.client.post(
            reverse('update_keranjang', args=[self.item.id]),
            {'quantity': 0}
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Jumlah harus lebih dari 0', str(messages[0]))

    def test_hapus_dari_keranjang_nonexistent_item(self):
        """Test removing non-existent item from cart"""
        non_existent_id = 99999
        response = self.client.post(
            reverse('hapus_dari_keranjang', args=[non_existent_id])
        )
        self.assertEqual(response.status_code, 404)

    def test_checkout_redirect_to_pengiriman(self):
        """Test checkout redirects to pengiriman with correct query params"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'keranjang_id={self.keranjang.id}', response.url)
        
    def test_tambah_ke_keranjang_ajax_success(self):
        """Test successful AJAX request to add item to cart"""
        response = self.client.post(
            reverse('tambah_ke_keranjang_ajax', args=[str(self.product.id)]),
            {'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
    def test_update_keranjang_ajax_success(self):
        """Test successful AJAX request to update cart item"""
        response = self.client.post(
            reverse('update_keranjang_ajax', args=[self.item.id]),
            {'quantity': 3},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
    def test_hapus_dari_keranjang_ajax_success(self):
        """Test successful AJAX request to remove item from cart"""
        response = self.client.post(
            reverse('hapus_dari_keranjang_ajax', args=[self.item.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])