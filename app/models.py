from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model. Extend later if needed."""


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Label({self.name})"


class Image(models.Model):
    file = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    labels = models.ManyToManyField(Label, related_name="images", blank=True)
    #TODO:
    # add 'status' field (with db_index=True ?)
    # add checksum ? -> models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Image({self.file.name})"
