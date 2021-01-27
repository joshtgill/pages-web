from django.db import models
from django.conf import settings


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    iconFileName = models.CharField(max_length=LENGTH_SHORT)


class Organization(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)


class CreatorUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
