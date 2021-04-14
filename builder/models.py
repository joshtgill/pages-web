from django.db import models
from django.conf import settings
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


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

    def deserialize(self, postData):
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

                sheetItem.deserialize(postData, i)
                sheetItem.save()
        elif postData.get('pageType')[0] == 'Event':
            event = None
            try:
                event = Event.objects.get(page=self)
            except ObjectDoesNotExist:
                event = Event(page=self)

            event.deserialize(postData)
            event.save()


    def serialize(self):
        data = model_to_dict(self)
        data.update({'organization': model_to_dict(self.organization)})

        if self.typee == 'Sheet':
            itemsData = []
            for sheetItem in SheetItem.objects.filter(page=self):
                itemsData.append(sheetItem.serialize())
            data.update({'items': itemsData})
        elif self.typee == 'Event':
            data.update({'event': Event.objects.get(page=self).serialize})

        return data


class SheetItem(models.Model):
    title = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)
    price = models.FloatField(null=True)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)

    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def deserialize(self, postData, postDataIndex):
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
            repeatingOccurence.deserialize(postData, postDataIndex)
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
            singleOccurence.deserialize(postData, postDataIndex)
            singleOccurence.save()

    def serialize(self):
        data = model_to_dict(self)
        try:
            singleOccurence = SingleOccurence.objects.get(sheetItem=self)
            data.update({'singleOccurence': singleOccurence.serialize()})
        except ObjectDoesNotExist:
            pass
        try:
            repeatingOccurence = RepeatingOccurence.objects.get(sheetItem=self)
            data.update({'repeatingOccurence': repeatingOccurence.serialize()})
        except ObjectDoesNotExist:
            pass

        return data


class Event(models.Model):
    description = models.CharField(max_length=LENGTH_MEDIUM)
    location = models.CharField(max_length=LENGTH_MEDIUM, null=True)
    attendanceIsPublic = models.BooleanField(default=False)
    acceptees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_acceptees')
    declinees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_declinees')

    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def deserialize(self, postData):
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
            repeatingOccurence.deserialize(postData)
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
            singleOccurence.deserialize(postData)
            singleOccurence.save()

    def serialize(self):
        data = model_to_dict(self)

        try:
            singleOccurence = SingleOccurence.objects.get(event=self)
            data.update({'singleOccurence': singleOccurence.serialize()})
        except ObjectDoesNotExist:
            pass

        try:
            repeatingOccurence = RepeatingOccurence.objects.get(event=self)
            data.update({'repeatingOccurence': repeatingOccurence.serialize()})
        except ObjectDoesNotExist:
            pass

        del data['acceptees']
        accepteesData = []
        for acceptee in self.acceptees.all():
            accepteesData.append({'fullName': acceptee.get_full_name()})
        data.update({'acceptees': accepteesData})

        del data['declinees']
        declineesData = []
        for declinee in self.declinees.all():
            declineesData.append({'fullName': declinee.get_full_name()})
        data.update({'declinees': declineesData})

        return data


class SingleOccurence(models.Model):
    startDatetime = models.DateTimeField()
    endDatetime = models.DateTimeField()

    sheetItem = models.ForeignKey(SheetItem, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def deserialize(self, postData, postDataIndex=0):
        self.startDatetime = postData.get('startDatetime')[postDataIndex]
        self.endDatetime = postData.get('endDatetime')[postDataIndex]

    def serialize(self):
        return model_to_dict(self)


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

    def deserialize(self, postData, postDataIndex=0):
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

    def serialize(self):
        return model_to_dict(self)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)


class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    relatedDate = models.DateField()
    approved = models.BooleanField(default=False)
