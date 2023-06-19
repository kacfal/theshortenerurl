from django.db import models


class URL(models.Model):
    original_url = models.URLField(unique=False)
    short_url = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_url
