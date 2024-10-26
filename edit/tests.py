from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Product

class editTest(TestCase):
    def test_edit_main_redirects_to_login(self):
        response = self.client.get(reverse('edit:show_edit_main'))
        self.assertEqual(response.status_code, 302)
        redirect_url = response['Location']
        self.assertTrue(redirect_url.startswith('/login'))
        self.assertIn('next=', redirect_url)


    # def test_main_using_main_template(self):
    #     response = Client().get('')
    #     self.assertTemplateUsed(response, 'main.html')

    # def test_nonexistent_page(self):
    #     response = Client().get('/random/')
    #     self.assertEqual(response.status_code, 404)

    # def test_strong_mood_user(self):
    #     now = timezone.now()
    #     mood = MoodEntry.objects.create(
    #       mood="LUMAYAN SENANG",
    #       time = now,
    #       feelings = "senang sih, cuman tadi baju aku basah kena hujan :(",
    #       mood_intensity = 8,
    #     )
    #     self.assertTrue(mood.is_mood_strong)
