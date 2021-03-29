from django.db import models
from django.conf import settings


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100


class NewOrganizationRequest(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Organization(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    private = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PageListing(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    dateCreated = models.DateField()
    typee = models.CharField(max_length=LENGTH_SHORT)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class SheetItem(models.Model):
    title = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)
    price = models.FloatField(null=True)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)
    startDatetime = models.DateTimeField(null=True)
    endDatetime = models.DateTimeField(null=True)

    page = models.ForeignKey(Page, on_delete=models.CASCADE)


class Event(models.Model):
    description = models.CharField(max_length=LENGTH_MEDIUM)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)
    startDatetime = models.DateTimeField(null=True)
    endDatetime = models.DateTimeField(null=True)
    acceptees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_acceptees')
    declinees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_declinees')

    page = models.ForeignKey(Page, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    relatedDate = models.DateField()
    approved = models.BooleanField(default=False)
