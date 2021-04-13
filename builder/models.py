from django.db import models
from django.conf import settings
import datetime
from django.core.exceptions import ObjectDoesNotExist


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
    typee = models.CharField(max_length=LENGTH_SHORT)
    dateCreated = models.DateField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def load(self, postData):
        self.name = postData.get('pageName')[0]
        self.typee = postData.get('pageType')[0]
        self.dateCreated = datetime.date.today()
        self.save()

        if postData.get('pageType')[0] == 'Sheet':
            try:
                for itemId in postData.get('itemIdsToDelete')[0].split('|'):
                    SheetItem.objects.get(id=itemId).delete()
            except ValueError:
                pass

            for i in range(len(postData.get('id'))):
                sheetItem = None
                try:
                    sheetItem = SheetItem.objects.get(id=int(postData.get('id')[i]))
                except ObjectDoesNotExist:
                    sheetItem = SheetItem(page=self)

                sheetItem.load(postData, i)
                sheetItem.save()
        elif postData.get('pageType')[0] == 'Event':
            event = None
            try:
                event = Event.objects.get(page=self)
            except ObjectDoesNotExist:
                event = Event(page=self)

            event.load(postData)
            event.save()


class SheetItem(models.Model):
    title = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)
    price = models.FloatField(null=True)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)

    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def load(self, postData, postDataIndex):
        self.title = postData.get('title')[postDataIndex]
        self.description = postData.get('description')[postDataIndex]
        self.price = postData.get('price')[postDataIndex] if postData.get('price')[postDataIndex] else None
        self.location = postData.get('location')[postDataIndex]

        if postData.get('selectedDays')[postDataIndex] or RepeatingOccurence.objects.filter(sheetItem=self).exists():
            repeatingOccurence = None
            try:
                repeatingOccurence = RepeatingOccurence.objects.get(sheetItem=self)
                if not postData.get('selectedDays')[0]:
                    repeatingOccurence.delete()
                    return
            except ObjectDoesNotExist:
                repeatingOccurence = RepeatingOccurence(sheetItem=self)
            repeatingOccurence.load(postData, postDataIndex)
            repeatingOccurence.save()
        elif postData.get('startDatetime')[postDataIndex] or SingleOccurence.objects.filter(sheetItem=self).exists():
            singleOccurence = None
            try:
                singleOccurence = SingleOccurence.objects.get(sheetItem=self)
                if not postData.get('startDatetime')[postDataIndex] and not postData.get('endDatetime')[postDataIndex]:
                    singleOccurence.delete()
                    return
            except ObjectDoesNotExist:
                singleOccurence = SingleOccurence(sheetItem=self)
            singleOccurence.load(postData, postDataIndex)
            singleOccurence.save()


class Event(models.Model):
    description = models.CharField(max_length=LENGTH_MEDIUM)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)
    attendanceIsPublic = models.BooleanField(default=False)
    acceptees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_acceptees')
    declinees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_declinees')

    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def load(self, postData):
        self.description = postData.get('description')[0]
        self.location = postData.get('location')[0]
        self.attendanceIsPublic = ('attendanceIsPublic' in postData)

        if postData.get('selectedDays')[0] or RepeatingOccurence.objects.filter(event=self).exists():
            repeatingOccurence = None
            try:
                repeatingOccurence = RepeatingOccurence.objects.get(event=self)
                if not postData.get('selectedDays')[0]:
                    repeatingOccurence.delete()
                    return
            except ObjectDoesNotExist:
                repeatingOccurence = RepeatingOccurence(event=self)
            repeatingOccurence.load(postData)
            repeatingOccurence.save()
        else:
            singleOccurence = None
            try:
                singleOccurence = SingleOccurence.objects.get(event=self)
                if not postData.get('startDatetime')[0] and not postData.get('endDatetime')[0]:
                    singleOccurence.delete()
                    return
            except ObjectDoesNotExist:
                singleOccurence = SingleOccurence(event=self)
            singleOccurence.load(postData)
            singleOccurence.save()


class SingleOccurence(models.Model):
    startDatetime = models.DateTimeField()
    endDatetime = models.DateTimeField()

    sheetItem = models.ForeignKey(SheetItem, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def load(self, postData, postDataIndex=0):
        self.startDatetime = postData.get('startDatetime')[postDataIndex]
        self.endDatetime = postData.get('endDatetime')[postDataIndex]


class RepeatingOccurence(models.Model):
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    startTime = models.TimeField()
    endTime = models.TimeField()
    startDate = models.DateField()
    endDate = models.DateField()

    sheetItem = models.ForeignKey(SheetItem, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def load(self, postData, postDataIndex=0):
        selectedDays = postData.get('selectedDays')[postDataIndex]
        self.monday = ('M' in selectedDays)
        self.tuesday = ('T' in selectedDays)
        self.wednesday = ('W' in selectedDays)
        self.thursday = ('TH' in selectedDays)
        self.friday = ('F' in selectedDays)
        self.saturday = ('S' in selectedDays)
        self.sunday = ('SU' in selectedDays)
        self.startTime = postData.get('startTime')[postDataIndex]
        self.endTime = postData.get('endTime')[postDataIndex]
        self.startDate = postData.get('startDate')[postDataIndex]
        self.endDate = postData.get('endDate')[postDataIndex]


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    relatedDate = models.DateField()
    approved = models.BooleanField(default=False)
