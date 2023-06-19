from django.urls import path
from .views import (
    CreateShortURLView,
    RetrieveOriginalURLView,
    RedirectToOriginalURLView,
)


urlpatterns = [
    path("shorten/", CreateShortURLView.as_view(), name="create_short_url"),
    path(
        "retrieve/<str:short_url>/",
        RetrieveOriginalURLView.as_view(),
        name="retrieve_original_url",
    ),
]
