from .models import *
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


def createPitch(request):
    return render(request, 'create_pitch.html')


@login_required
def selectOrganization(request):
    organizations = Organization.objects.all()
    content = {'selectOrganizationForm': SelectOrganizationForm(organizations=organizations)}
    if request.method == 'GET':
        return render(request, 'select_organization.html', content)

    selectOrganizationForm = SelectOrganizationForm(request.POST, organizations=organizations)
    if not selectOrganizationForm.is_valid():
        return redirect('/create/select/')

    organization = Organization.objects.get(id=selectOrganizationForm.cleaned_data['ids'])
    request.user.profile.organization = organization
    if not Membership.objects.filter(user=request.user, organization=organization).exists():
        membership = Membership(user=request.user, organization=organization, relatedDate=datetime.date.today(), approved=True)
        membership.save()

    request.user.profile.save()

    return redirect('/create/')


@login_required
def requestNewOrganization(request):
    if request.method == 'GET':
        return render(request, 'request_new_organization.html', {'requestNewOrganizationForm': RequestNewOrganizationForm()})

    requestNewOrganizationForm = RequestNewOrganizationForm(request.POST)
    if not requestNewOrganizationForm.is_valid():
        return redirect('/create/request/')

    newOrganizationRequest = NewOrganizationRequest(name=requestNewOrganizationForm.cleaned_data['name'])
    newOrganizationRequest.applicant = request.user
    newOrganizationRequest.save()

    return redirect('/profile/')


@login_required
def build(request):
    if request.method == 'GET':
        pageListings = PageListing.objects
        buildForm = BuildForm(request.GET)

        if not buildForm.is_valid():
            # Page type isn't provided, list available Pages
            return render(request, 'select_page_type.html', {'pageListings': pageListings.all()})

        pageType = buildForm.cleaned_data['typee']
        if not pageListings.filter(name=pageType).count():
            return redirect('/create/build/')

        content = {}
        pageId = buildForm.cleaned_data['idd']
        if pageId and Page.objects.filter(organization=request.user.profile.organization, id=pageId).count():
            # Page ID is provided and belongs to active organization. Load Page builder with existing data.
            pageData = buildPageData(pageType, pageId)
            content.update({'pageData': pageData,
                            'pageDeleteConfirmationPopupData': {'prompt': 'Permanently delete <b>{}</b> from {}?'.format(pageData.get('name'),
                                                                                                                         request.user.profile.organization.name),
                                                                'confirmButtonText': 'Delete',
                                                                'formName': 'pageIdToDelete',
                                                                'formValue': pageData.get('id'),
                                                                'dismissButtonText': 'Cancel'}})
        else:
            # Invalid Page ID is provided with respect to organization. Load empty Page builder.
            content.update({'pageData': {'typee': pageType}})

        return render(request, 'build_page.html', content)

    deletePageForm = DeletePageForm(request.POST)
    if deletePageForm.is_valid():
        Page.objects.get(id=deletePageForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/manage/')

    pagePostData = dict(request.POST)

    # Handle updates for 'parent' Page
    page = handlePageUpdate(request, pagePostData)

    # Handle updates for specific Page
    pageType = pagePostData.get('pageType')[0]
    if pageType == 'Sheet':
        handleSheetItemsUpdates(pagePostData, page)
    elif pageType == 'Event':
        handleEventUpdate(pagePostData, page)

    return redirect('/create/manage/')


def buildPageData(pageType, idd):
    page = Page.objects.get(id=idd)
    pageData = model_to_dict(page)
    if pageType == 'Sheet':
        sheetItemsData = []
        for sheetItem in SheetItem.objects.filter(page=page):
            sheetItemData = model_to_dict(sheetItem)
            if RepeatingOccurence.objects.filter(sheetItem=sheetItem).exists():
                sheetItemData.update({'repeating': model_to_dict( RepeatingOccurence.objects.get(sheetItem=sheetItem))})
            sheetItemsData.append(sheetItemData)
        pageData.update({'items': sheetItemsData})
    elif pageType == 'Event':
        eventData = model_to_dict(Event.objects.get(page=page))
        del eventData['acceptees']
        del eventData['declinees']
        pageData.update({'event': eventData})

    return pageData


def handlePageUpdate(request, pagePostData):
    page = None
    try:
        page = Page.objects.get(id=pagePostData.get('pageId')[0])
        page.name = pagePostData.get('pageName')[0]
    except ValueError:
        page = Page(name=pagePostData.get('pageName')[0], typee=pagePostData.get('pageType')[0], dateCreated=datetime.date.today())
        page.organization = request.user.profile.organization
    page.save()

    return page


def handleSheetItemsUpdates(pagePostData, page):
    try:
        for sheetItemId in pagePostData.get('itemIdsToDelete')[0].split('|'):
            SheetItem.objects.get(id=int(sheetItemId)).delete()
    except ValueError:
        pass

    ids = pagePostData.get('id')
    titles = pagePostData.get('title')
    descriptions = pagePostData.get('description')
    prices = pagePostData.get('price')
    locations = pagePostData.get('location')
    startDatetimes = pagePostData.get('startDatetime')
    endDatetimes = pagePostData.get('endDatetime')
    selectedDays = pagePostData.get('selectedDays')
    startTimes = pagePostData.get('startTime')
    endTimes = pagePostData.get('endTime')
    startDates = pagePostData.get('startDate')
    endDates = pagePostData.get('endDate')
    for i in range(len(ids)):
        try:
            sheetItem = SheetItem.objects.get(id=int(ids[i]))
            sheetItem.title = titles[i]
            sheetItem.description = descriptions[i]
            sheetItem.price = prices[i] if prices[i] else None
            sheetItem.location = locations[i] if locations[i] else None
            sheetItem.startDatetime = startDatetimes[i] if startDatetimes[i] else None
            sheetItem.endDatetime = endDatetimes[i] if endDatetimes[i] else None
            sheetItem.save()
            if selectedDays[i] or RepeatingOccurence.objects.filter(sheetItem=sheetItem).exists():
                repeatingOccurence = None
                try:
                    repeatingOccurence = RepeatingOccurence.objects.get(sheetItem=sheetItem)
                    if not selectedDays[i]:
                        repeatingOccurence.delete()
                        return
                except ObjectDoesNotExist:
                    repeatingOccurence = RepeatingOccurence(sheetItem=sheetItem)
                days = selectedDays[i].split('|')
                repeatingOccurence.monday=('M' in days)
                repeatingOccurence.tuesday=('T' in days)
                repeatingOccurence.wednesday=('W' in days)
                repeatingOccurence.thursday=('TH' in days)
                repeatingOccurence.friday=('F' in days)
                repeatingOccurence.saturday=('S' in days)
                repeatingOccurence.sunday=('SU' in days)
                repeatingOccurence.startTime=startTimes[i]
                repeatingOccurence.endTime=endTimes[i]
                repeatingOccurence.startDate=startDates[i]
                repeatingOccurence.endDate=endDates[i]
                repeatingOccurence.save()

        except ObjectDoesNotExist:
            sheetItem = SheetItem(title=titles[i], description=descriptions[i])
            sheetItem.location = locations[i] if locations[i] else None
            sheetItem.price = prices[i] if prices[i] else None
            sheetItem.startDatetime = startDatetimes[i]
            sheetItem.endDatetime = endDatetimes[i]
            sheetItem.page = page
            sheetItem.save()
            if selectedDays[i]:
                days = selectedDays[i].split('|')
                RepeatingOccurence(monday=('M' in days),
                                   tuesday=('T' in days),
                                   wednesday=('W' in days),
                                   thursday=('TH' in days),
                                   friday=('F' in days),
                                   saturday=('S' in days),
                                   sunday=('SU' in days),
                                   startTime=startTimes[i],
                                   endTime=endTimes[i],
                                   startDate=startDates[i],
                                   endDate=endDates[i],
                                   sheetItem=sheetItem).save()


def handleEventUpdate(pagePostData, page):
    description = pagePostData.get('description')[0]
    location = pagePostData.get('location')[0]
    startDatetime = pagePostData.get('startDatetime')[0]
    endDatetime = pagePostData.get('endDatetime')[0]
    attendanceIsPublic = False
    try:
        attendanceIsPublic = bool(pagePostData.get('attendanceIsPublic')[0])
    except TypeError:
        pass

    event = None
    try:
        event = Event.objects.get(page=page)
        event.description = description
        event.location = location
        event.startDatetime = startDatetime
        if endDatetime:
            event.endDatetime = endDatetime
        event.attendanceIsPublic = attendanceIsPublic
    except Exception:
        event = Event(description=description,
                      location=location,
                      startDatetime=startDatetime,
                      attendanceIsPublic=attendanceIsPublic,
                      page=page)
        if endDatetime:
            event.endDatetime = endDatetime
    event.save()


@login_required
def manageOrganization(request):
    if request.method == 'GET':
        content = {'numOrganizationsMemberships': len(Membership.objects.filter(organization=request.user.profile.organization, approved=True)),
                   'activePagesData': buildOrganizationsPagesData(request.user.profile.organization),
                   'memberRequests': Membership.objects.filter(approved=False)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'organizationMembers': Membership.objects.filter(organization=request.user.profile.organization, approved=True)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'approveMembershipConfirmationPopupData': {'prompt': None,
                                                              'confirmButtonText': 'Approve',
                                                              'formName': 'membershipIdToApprove',
                                                              'formValue': None,
                                                              'dismissButtonText': 'Cancel'},
                   'denyMembershipConfirmationPopupData': {'prompt': None,
                                                           'confirmButtonText': 'Deny',
                                                           'formName': 'membershipIdToDeny',
                                                           'formValue': None,
                                                           'dismissButtonText': 'Cancel'},
                   'revokeMembershipConfirmationPopupData': {'prompt': None,
                                                             'confirmButtonText': 'Revoke',
                                                             'formName': 'membershipIdToRevoke',
                                                             'formValue': None,
                                                             'dismissButtonText': 'Cancel'},
                   'leaveOrganizationConfirmationPopupData': {'prompt': 'Leave <b>{}</b>?'.format(request.user.profile.organization.name),
                                                              'confirmButtonText': 'Leave',
                                                              'formName': 'leaveOrganization',
                                                              'formValue': True,
                                                              'dismissButtonText': 'Cancel'},
                   'deleteOrganizationConfirmationPopupData': {'prompt': 'Delete <b>{}</b>?'.format(request.user.profile.organization.name),
                                                               'confirmButtonText': 'Delete',
                                                               'formName': 'deleteOrganization',
                                                               'formValue': True,
                                                               'dismissButtonText': 'Cancel'}}
        return render(request, 'manage_organization.html', content)

    leaveOrganizationForm = LeaveOrganizationForm(request.POST)
    if leaveOrganizationForm.is_valid() and request.user.profile.organization.owner != request.user:
        request.user.profile.organization = None
        request.user.profile.save()
        return redirect('/')

    deleteOrganizationForm = DeleteOrganizationForm(request.POST)
    if deleteOrganizationForm.is_valid():
        request.user.profile.organization.delete()
        return redirect('/')

    approveMembershipForm = ApproveMembershipForm(request.POST)
    if approveMembershipForm.is_valid():
        membership = Membership.objects.get(id=approveMembershipForm.cleaned_data['membershipIdToApprove'])
        membership.relatedDate = datetime.date.today()
        membership.approved = True
        membership.save()
        return redirect('/create/manage/')

    denyMembershipForm = DenyMembershipForm(request.POST)
    if denyMembershipForm.is_valid():
        Membership.objects.get(id=denyMembershipForm.cleaned_data['membershipIdToDeny']).delete()
        return redirect('/create/manage/')

    revokeMembershipForm = RevokeMembershipForm(request.POST)
    if revokeMembershipForm.is_valid():
        Membership.objects.get(id=revokeMembershipForm.cleaned_data['membershipIdToRevoke']).delete()

    return redirect('/create/manage/')


def buildOrganizationsPagesData(organization):
    organizationsPagesData = []
    for page in Page.objects.filter(organization=organization)[:settings.MAX_DASHBOARD_LIST_ENTRIES]:
        organizationsPagesData.append({'id': page.id, 'name': page.name, 'type': page.typee,
                                       'dateCreated': page.dateCreated.strftime("%B %d, %Y"),
                                       'numItems': len(SheetItem.objects.filter(page=page))})

    return organizationsPagesData


@login_required
def editOrganization(request):
    if request.method == 'POST':
        editOrganizationForm = EditOrganizationForm(request.POST)
        if editOrganizationForm.is_valid():
            request.user.profile.organization.name = editOrganizationForm.cleaned_data['name']
            request.user.profile.organization.private = editOrganizationForm.cleaned_data['private']
            request.user.profile.organization.save()
        return redirect('/create/manage/')

    return render(request, 'edit_organization.html')
