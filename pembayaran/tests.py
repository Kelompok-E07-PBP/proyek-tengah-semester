from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Pembayaran
from pengiriman.models import Pengiriman
from keranjang.models import Keranjang, ItemKeranjang
from main.models import Product
from decimal import Decimal

class PembayaranTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        self.product = Product.objects.create(
            nama_produk="Test Product",
            harga=Decimal('100000.00'),
            kategori="Dasi Instant",
            gambar_produk="http://example.com/image.jpg"
        )

        self.pengiriman = Pengiriman.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone_number="1234567890",
            address="Test Address",
            city="Jakarta Barat",
            postal_code="12345",
            courier="JNE"
        )

        self.pembayaran_url = reverse("pembayaran:pembayaran_view")
        self.process_payment_url = reverse("pembayaran:process_payment_ajax")

        self.create_cart_with_items()

    def create_cart_with_items(self):
        Keranjang.objects.filter(user=self.user).delete()
        self.keranjang = Keranjang.objects.create(user=self.user)
        self.item = ItemKeranjang.objects.create(
            keranjang=self.keranjang,
            product=self.product,
            quantity=2
        )

    def test_pembayaran_view_get(self):
        response = self.client.get(self.pembayaran_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pembayaran.html")
        self.assertIn("keranjang_items", response.context)
        self.assertIn("pengiriman", response.context)
        self.assertIn("total_harga", response.context)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["pengiriman"].city, "Jakarta Barat")
        self.assertEqual(response.context["delivery_fee"], 10000)

    def test_pembayaran_view_post_without_cart_items(self):
        self.keranjang.itemkeranjang_set.all().delete()
        response = self.client.post(self.pembayaran_url, {"payment_method": "Kartu Kredit"})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Keranjang kosong atau informasi pengiriman tidak lengkap.", status_code=400)

    def test_process_payment_ajax_with_valid_data(self):
        self.create_cart_with_items()

        keranjang_total = Decimal(self.keranjang.get_total())
        delivery_fee = Decimal("10000.00")
        total_harga = keranjang_total + delivery_fee

        response = self.client.post(
            self.process_payment_url,
            {"payment_method": "Kartu Kredit"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Payment successful!")

        pembayaran = Pembayaran.objects.filter(user=self.user).latest('created_at')
        pembayaran.refresh_from_db()

        self.assertEqual(pembayaran.amount, total_harga)
        self.assertFalse(self.keranjang.itemkeranjang_set.exists())

    def test_process_payment_ajax_without_shipping_info(self):
        self.pengiriman.delete()
        response = self.client.post(
            self.process_payment_url,
            {"payment_method": "Kartu Kredit"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Informasi pengiriman tidak lengkap.")

    def test_process_payment_ajax_without_payment_method(self):
        response = self.client.post(
            self.process_payment_url,
            {},  
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Please select a payment method.")

    def test_show_json_view(self):
        pembayaran = Pembayaran.objects.create(
            user=self.user,
            amount=Decimal("200000.00"),
            payment_method="Kartu Kredit"
        )
        json_url = reverse("pembayaran:show_json_pembayaran")
        response = self.client.get(json_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, pembayaran.payment_method)
        self.assertContains(response, str(pembayaran.amount))

    def test_direct_pembayaran_creation(self):
        pembayaran = Pembayaran.objects.create(
            user=self.user,
            amount=Decimal("210000.00"),
            payment_method="Kartu Kredit"
        )
        pembayaran.refresh_from_db()
        self.assertEqual(pembayaran.amount, Decimal("210000.00"))
