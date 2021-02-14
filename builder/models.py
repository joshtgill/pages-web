from django.db import models
from django.conf import settings


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)


class Organization(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)


class Sheet(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class SheetItem(models.Model):
    title = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)
    price = models.FloatField()

    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)


class CreatorUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
