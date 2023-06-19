from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.response import Response

from .models import URL
from .serializers import URLSerializer


class CreateShortURLView(generics.CreateAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = self.generate_short_url()
        serializer.save(short_url=short_url)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"short_url": short_url}, status=status.HTTP_201_CREATED, headers=headers
        )

    def generate_short_url(self):
        while True:
            short_url = get_random_string(length=8)
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url


class RetrieveOriginalURLView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = "short_url"
    lookup_url_kwarg = "short_url"


class RedirectToOriginalURLView(generics.RetrieveAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    lookup_field = "short_url"
    lookup_url_kwarg = "short_url"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return redirect(instance.original_url)
