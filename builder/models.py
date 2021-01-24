from django.db import models
from django.conf import settings


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    iconFileName = models.CharField(max_length=LENGTH_SHORT)


class CreatorUser(models.Model):
    organization = models.CharField(max_length=LENGTH_MEDIUM)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
