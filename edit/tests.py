from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Product
from django.contrib.auth import get_user_model
from edit.forms import ProductForm
from django.core import serializers
import json

class editTest(TestCase):

    # Memanggil fungsi setup lainnya
    def setUp(self):
        self.setUpUser()
        self.setUpProduct()

    # Setup sebuah superuser bernama dummyadmin dan user biasa bernama dummy1
    def setUpUser(self):
        self.superuser = get_user_model().objects.create_superuser(
            username='dummyadmin',
            password='TiDA,tmdoAa.',
        )
        self.normal_user = get_user_model().objects.create_user(
            username='dummy1',
            password='HID1,Ijadft.'
        )

    # Membuat suatu instance product untuk uji coba.
    def setUpProduct(self):
        self.product = Product.objects.create(
            nama_produk='DRM8-B01',
            kategori='Dasi Instant',
            harga=30000,
            gambar_produk='https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        )

    # Menguji apakah user kena redirect ke login kalau coba akses bagian ini.
    def test_edit_main_redirects_to_login(self):
        response = self.client.get(reverse('edit:show_edit_main'))
        self.assertEqual(response.status_code, 302)
        redirect_url = response['Location']
        self.assertTrue(redirect_url.startswith('/login'))
        self.assertIn('next=', redirect_url)

    # Uji coba apakah superuser akan redirect ke halaman edit
    def test_show_edit_main_superuser(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        self.client.cookies['last_login'] = 'some_value'
        response = self.client.get(reverse('edit:show_edit_main'))
        self.assertEqual(response.status_code, 200)

    # Uji coba apakah user biasa akan dapat status 404 dan redirect ke forbidden_view
    def test_show_edit_main_normal_user(self):
        self.client.login(username='dummy1', password='HID1,Ijadft.')
        response = self.client.get(reverse('edit:show_edit_main'))
        self.assertEqual(response.status_code, 302)

    def test_forbidden_view(self):
        response = self.client.get(reverse('edit:forbidden_view'))
        self.assertEqual(response.status_code, 404)

    # Uji coba entry form yang valid dan tidak valid.
    def test_create_product_entry_valid(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        response = self.client.post(reverse('edit:create_product_entry'), {
            'nama_produk': 'DRM8-B01',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(nama_produk='DRM8-B01').exists())

    def test_create_product_entry_invalid(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        response = self.client.post(reverse('edit:create_product_entry'), {
            'nama_produk': '',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    # Uji coba edit product yang valid dan tidak valid.
    def test_edit_product_entry_valid(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        product = Product.objects.create(nama_produk='DRM8-B01', kategori='Dasi Instant', harga=35000, gambar_produk='https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp')

        response = self.client.post(reverse('edit:edit_product_entry', args=[product.id]), {
            'nama_produk': 'DRM8-B01',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp',
        })
        self.assertEqual(response.status_code, 302)
        product.refresh_from_db()
        self.assertEqual(product.nama_produk, 'DRM8-B01')

    def test_edit_product_entry_invalid(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        product = Product.objects.create(nama_produk='DRM8-B01', kategori='Dasi Instant', harga=30000, gambar_produk='https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp')

        response = self.client.post(reverse('edit:edit_product_entry', args=[product.id]), {
            'nama_produk': '',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    # Uji coba delete sebuah produk
    def test_delete_product_entry(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        product = Product.objects.create(nama_produk='DRM8-B01', kategori='Dasi Instant', harga=30000, gambar_produk='https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp')

        response = self.client.post(reverse('edit:delete_product_entry', args=[product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=product.id).exists())

    # Uji coba menambahkan sebuah produk secara AJAX.
    def test_add_product_entry_ajax(self):
        self.client.login(username='dummyadmin', password='TiDA,tmdoAa.')
        response = self.client.post(reverse('edit:add_product_entry_ajax'), {
            'nama_produk': 'DRM8-B01',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp',
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(nama_produk='DRM8-B01').exists())

    # Uji coba show_json dari produk.
    def test_show_json(self):
        response = self.client.get(reverse('edit:show_json'))
        self.assertEqual(response.status_code, 200)
        
        expected_data = [{
            'model': 'main.product',
            'pk': str(self.product.pk),
            'fields': {
                'nama_produk': 'DRM8-B01',
                'kategori': 'Dasi Instant',
                'harga': '30000.00',
                'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
            }
        }]
        
        actual_data = json.loads(response.content)
        self.assertEqual(actual_data, expected_data)

    # Uji coba memasukkan data valid ke dalam forms.py dan lihat apakah hasilnya tetap sama.
    def test_valid_form(self):
        form_data = {
            'nama_produk': 'DRM8-B01',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        }
        form = ProductForm(data=form_data, instance=self.product)
        self.assertTrue(form.is_valid())
        product = form.save()

        self.assertEqual(product.nama_produk, 'DRM8-B01')
        self.assertEqual(product.kategori, 'Dasi Instant')
        self.assertEqual(product.harga, 30000)
        self.assertEqual(product.gambar_produk, 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp')

    # Uji coba mengosongkan nama_produk dalam forms.py dan lihat apakah gagal.
    def test_invalid_form_missing_nama_produk(self):
        form_data = {
            'nama_produk': '',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        }
        form = ProductForm(data=form_data, instance=self.product)
        self.assertFalse(form.is_valid())
        self.assertIn('nama_produk', form.errors)

    # Uji coba memasukkan harga tidak valid ke dalam forms.py dan lihat apakah gagal.
    def test_invalid_form_harga(self):
        form_data = {
            'nama_produk': '',
            'kategori': 'Dasi Instant',
            'harga': 'a',
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        }
        form = ProductForm(data=form_data, instance=self.product)
        self.assertFalse(form.is_valid())
        self.assertIn('nama_produk', form.errors)

    # Uji coba strip tags pada form
    def test_clean_nama_produk_removes_tags(self):
        form_data = {
            'nama_produk': '<p>DRM8-B01</p>',
            'kategori': 'Dasi Instant',
            'harga': 30000,
            'gambar_produk': 'https://down-id.img.susercontent.com/file/sg-11134201-23020-unxcmwqsignv6a@resize_w450_nl.webp'
        }
        form = ProductForm(data=form_data, instance=self.product)
        form.is_valid()
        self.assertEqual(form.cleaned_data['nama_produk'], 'DRM8-B01')
