from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import django.contrib.auth as djangoAuth
import uuid
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


LENGTH_SHORT = 30
LENGTH_MEDIUM = 100
LENGTH_LONG= 300


def create(self, request, email, password, passwordConfirm, firstName, lastName):
    if User.objects.filter(email=email).exists():
        return {'error': {'message': 'Failed to create account - an account with the email \'{}\' already exists.'.format(email),
                          'link': {'path': '/login/', 'text': 'Login'}}}
    elif password != passwordConfirm:
        return {'error': {'message': 'Failed to create account - passwords did not match'}}

    self.username = uuid.uuid4()
    self.email = email
    self.password = password
    self.first_name = firstName
    self.last_name = lastName
    self.save()

    profile = Profile(user=self)
    profile.save()

    djangoAuth.login(request, self)

    return None
User.add_to_class('create', create)

def login(self, request, email, password):
    username = None
    try:
        username = User.objects.get(email=email).username
    except ObjectDoesNotExist:
        return {'error': {'message': 'Failed to login - an account with the email \'{}\' does not exist.'.format(email),
                          'link': {'path': '/create-account/', 'text': 'Create an account'}}}

    self = djangoAuth.authenticate(request, username=username, password=password)
    if not self:
        return {'error': {'message': 'Failed to login - incorrect password'}}

    djangoAuth.login(request, self)

    return None
User.add_to_class('login', login)

def changeEmail(self, newEmail, newEmailConfirm):
    if newEmail != newEmailConfirm:
        return {'error': {'message': 'Failed to change email - emails did not match'}}

    self.email = newEmail
    self.save()

    return None
User.add_to_class('changeEmail', changeEmail)

def deletee(self, request):
    djangoAuth.logout(request)
    self.delete()
    pass
User.add_to_class('deletee', deletee)


class NewOrganizationRequest(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Organization(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_LONG)
    isPrivate = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # SET_NULL? Orphan Organization?

    def create(self, approvedRequest):
        self.name = approvedRequest.name
        self.isPrivate = False
        self.owner = approvedRequest.applicant
        self.save()

        # Create the membership
        Membership().create(self, approvedRequest.applicant, True)

        # Owner is always member
        approvedRequest.applicant.profile.organization = self
        approvedRequest.applicant.profile.save()

        # Delete the fulfilled request
        approvedRequest.delete()

    def getPagesData(self):
        pagesData = []
        for page in Page.objects.filter(organization=self)[:settings.MAX_DASHBOARD_LIST_ENTRIES]:
            pagesData.append(page.serialize(False))

        return pagesData

    def deserialize(self, data):
        self.name = data['name']
        self.description = data['description']
        self.isPrivate = data['isPrivate']
        self.save()


class PageListing(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    description = models.CharField(max_length=LENGTH_MEDIUM)


class Page(models.Model):
    name = models.CharField(max_length=LENGTH_SHORT)
    explanation = models.CharField(max_length=LENGTH_LONG)
    typee = models.CharField(max_length=LENGTH_SHORT)
    dateCreated = models.DateField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def deserialize(self, postData):
        self.name = postData.get('pageName')[0]
        self.description = postData.get('pageExplanation')[0]
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
        elif postData.get('pageType')[0] == 'Event':
            event = None
            try:
                event = Event.objects.get(page=self)
            except ObjectDoesNotExist:
                event = Event(page=self)

            event.deserialize(postData)

    def serialize(self, recursive=True):
        data = model_to_dict(self)
        if not recursive:
            return data

        if self.typee == 'Sheet':
            itemsData = []
            for sheetItem in SheetItem.objects.filter(page=self):
                itemsData.append(sheetItem.serialize())
            data.update({'items': itemsData})
        elif self.typee == 'Event':
            data.update({'event': Event.objects.get(page=self).serialize()})

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
        self.save()

        if postData.get('selectedDays')[postDataIndex] or RepeatingOccurence.objects.filter(sheetItem=self).exists():
            repeatingOccurence = None
            try:
                repeatingOccurence = RepeatingOccurence.objects.get(sheetItem=self)
                if not postData.get('selectedDays')[postDataIndex]:
                    repeatingOccurence.delete()
                    return
            except ObjectDoesNotExist:
                repeatingOccurence = RepeatingOccurence(sheetItem=self)
            repeatingOccurence.deserialize(postData, postDataIndex)
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

    def updateAttendance(self, user, status):
        self.acceptees.remove(user)
        self.declinees.remove(user)

        if status:
            self.acceptees.add(user)
        else:
            self.declinees.add(user)

        self.save()

    def deserialize(self, postData):
        self.description = postData.get('description')[0]
        self.location = postData.get('location')[0]
        self.attendanceIsPublic = ('attendanceIsPublic' in postData)
        self.save()

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
            accepteesData.append(acceptee.get_full_name())
        data.update({'acceptees': accepteesData})

        del data['declinees']
        declineesData = []
        for declinee in self.declinees.all():
            declineesData.append(declinee.get_full_name())
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
        self.save()

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
        selectedDays = postData.get('selectedDays')[postDataIndex].split('|')
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
        self.save()

    def serialize(self):
        return model_to_dict(self)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)


class MembershipManager(models.Manager):
    def create(self, organization, user, approved):
        if self.filter(organization=organization, user=user).exists():
            return False

        self.create(organization=organization,
                    user=user,
                    relatedDate=datetime.date.today(),
                    approved=approved)

        return True

    def delete(self, id):
        self.get(id=id).delete()

class Membership(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    relatedDate = models.DateField()
    approved = models.BooleanField(default=False)

    objects = MembershipManager()

    def approve(self):
        self.approved = True
        self.relatedDate = datetime.date.today()
        self.save()
