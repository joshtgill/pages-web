from django.db import models
from django.conf import settings


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100


class OrganizationApplication(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Organization(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    private = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class OrganizationApproval(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    approvee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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
    price = models.FloatField()

    page = models.ForeignKey(Page, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    memberships = models.ManyToManyField(Organization, related_name='organizationMemberships')
