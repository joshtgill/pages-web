from django.db import models


LENGTH_SHORT = 30


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    iconFileName = models.CharField(max_length=LENGTH_SHORT)
