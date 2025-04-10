from django.db import models
from django.utils import timezone


class Trait(models.Model):
    trait_name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
