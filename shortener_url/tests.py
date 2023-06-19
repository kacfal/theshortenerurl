from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import URL


class URLShortenerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_short_url(self):
        url = "http://example.com/very-very/long/url/even-longer"
        response = self.client.post(reverse("create_short_url"), {"original_url": url})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)

        short_url = response.data["short_url"]
        self.assertTrue(URL.objects.filter(short_url=short_url).exists())

    def test_retrieve_original_url(self):
        url = "http://example.com/very-very/long/url/even-longer"
        new_url = URL.objects.create(original_url=url, short_url="my-random-string")

        response = self.client.get(
            reverse("retrieve_original_url", args=["my-random-string"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("original_url", response.data)
        self.assertEqual(response.data["original_url"], url)

    def test_redirect_to_original_url(self):
        url = "http://example.com/very-very/long/url/even-longer"
        new_url = URL.objects.create(original_url=url, short_url="my-random-string")

        response = self.client.get(
            reverse("redirect_to_original_url", args=["my-random-string"])
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, url)

    def test_invalid_short_url(self):
        response = self.client.get(
            reverse("redirect_to_original_url", args=["invalid-url"])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
