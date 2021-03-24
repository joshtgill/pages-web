from .models import *
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


def create(request):
    return render(request, 'create_pitch.html')


@login_required
def selectOrganization(request):
    organizations = Organization.objects.all()
    content = {'selectOrganizationForm': SelectOrganizationForm(organizations=organizations)}
    if request.method == 'GET':
        return render(request, 'select_organization.html', content)

    selectOrganizationForm = SelectOrganizationForm(request.POST, organizations=organizations)
    if not selectOrganizationForm.is_valid():
        return render(request, 'select_organization.html', content)

    request.user.profile.organization = Organization.objects.get(id=selectOrganizationForm.cleaned_data['ids'])
    request.user.profile.save()

    return redirect('/create/')


@login_required
def applyOrganization(request):
    if request.method == 'GET':
        return render(request, 'apply_organization.html', {'applyOrganizationForm': ApplyOrganizationForm()})

    applyOrganizationForm = ApplyOrganizationForm(request.POST)
    if not applyOrganizationForm.is_valid():
        return redirect('/create/apply/')

    organizationApplication = OrganizationApplication(name=applyOrganizationForm.cleaned_data['name'])
    organizationApplication.applicant = request.user
    organizationApplication.save()

    return redirect('/profile/')


@login_required
def builder(request):
    if request.method == 'GET':
        pageListings = PageListing.objects
        builderForm = BuilderForm(request.GET)

        # If a Page type isn't provided, list available Page types
        if not builderForm.is_valid():
            return render(request, 'builder_select_type.html', {'pageListings': pageListings.all()})

        # If the provided Page type doesn't exist, list available Pages
        pageType = builderForm.cleaned_data['typee']
        if not pageListings.filter(name=pageType).count():
            return render(request, 'builder.html', {'pageListings': pageListings.all()})

        # If a Page ID is provided that also belongs to the active organization, load existing data
        # If only a Page ID is provided, redirect to a new Page
        # Otherwise only provide the type of Page
        content = {}
        pageId = builderForm.cleaned_data['idd']
        if pageId and Page.objects.filter(organization=request.user.profile.organization, id=pageId).count():
            pageData = buildPageData(pageId)
            content.update({'pageData': pageData,
                            'pageDeleteConfirmationPopupData': {'prompt': 'Permanently delete <b>{}</b> from {}?'.format(pageData.get('name'),
                                                                                                                         request.user.profile.organization.name),
                                                                'confirmButtonText': 'Delete',
                                                                'formName': 'pageIdToDelete',
                                                                'formValue': pageData.get('id'),
                                                                'dismissButtonText': 'Cancel'}})
        elif pageId:
            return redirect('/create/builder/?typee={}'.format(pageType))
        else:
            content.update({'pageData': {'typee': pageType}})

        return render(request, 'builder_page.html', content)

    pageDeleteForm = PageDeleteForm(request.POST)
    if pageDeleteForm.is_valid():
        Page.objects.get(id=pageDeleteForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/manage/')

    pagePostData = dict(request.POST)
    page = handlePageUpdate(request, pagePostData)
    handleSheetItemsUpdates(pagePostData, page)

    return redirect('/create/manage/')


def buildPageData(idd):
    page = Page.objects.get(id=idd)
    pageData = model_to_dict(page)

    sheetItemsData = []
    for sheetItem in SheetItem.objects.filter(page=page):
        sheetItemsData.append(model_to_dict(sheetItem))
    pageData.update({'items': sheetItemsData})

    return pageData


def handlePageUpdate(request, pagePostData):
    # If the Page exists, update its name. Otherwise create it.
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
    # Delete marked items
    try:
        for sheetItemId in pagePostData.get('itemIdsToDelete')[0].split('|'):
            SheetItem.objects.get(id=int(sheetItemId)).delete()
    except ValueError:
        pass

    # For each Sheet Item, update its attributes if it exists. Otherwise create it.
    sheetItemIds = pagePostData.get('id')
    if not sheetItemIds:
        return

    sheetItemTitles = pagePostData.get('title')
    sheetItemDescriptions = pagePostData.get('description')
    sheetItemPrices = pagePostData.get('price')
    sheetItemStartDatetimes = pagePostData.get('startDatetime')
    sheetItemEndDatetimes = pagePostData.get('endDatetime')
    for i in range(len(sheetItemIds)):
        try:
            sheetItem = SheetItem.objects.get(id=int(sheetItemIds[i]))
            sheetItem.title = sheetItemTitles[i]
            sheetItem.description = sheetItemDescriptions[i]
            sheetItem.price = sheetItemPrices[i] if sheetItemPrices[i] else None
            sheetItem.startDatetime = sheetItemStartDatetimes[i] if sheetItemStartDatetimes[i] else None
            sheetItem.endDatetime = sheetItemEndDatetimes[i] if sheetItemEndDatetimes[i] else None

        except ObjectDoesNotExist:
            sheetItem = SheetItem(title=sheetItemTitles[i], description=sheetItemDescriptions[i])
            sheetItem.price = sheetItemPrices[i] if sheetItemPrices[i] else None

            sheetItem.startDatetime = (datetime.datetime.strptime(sheetItemStartDatetimes[i], '%Y-%m-%dT%H:%M')
                                       if sheetItemStartDatetimes[i] else None)
            sheetItem.endDatetime = (datetime.datetime.strptime(sheetItemEndDatetimes[i], '%Y-%m-%dT%H:%M')
                                     if sheetItemEndDatetimes[i] else None)

            sheetItem.page = page
        sheetItem.save()


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
                                                              'dismissButtonText': 'Cancel'}}
        return render(request, 'manage_organization.html', content)

    leaveOrganizationForm = LeaveOrganizationForm(request.POST)
    if leaveOrganizationForm.is_valid() and request.user.profile.organization.owner != request.user:
        request.user.profile.organization = None
        request.user.profile.save()
        return redirect('/')

    approveMembershipForm = ApproveMembershipForm(request.POST)
    if approveMembershipForm.is_valid():
        # Approve the membership
        membership = Membership.objects.get(id=approveMembershipForm.cleaned_data['membershipIdToApprove'])
        membership.relatedDate = datetime.date.today()
        membership.approved = True
        membership.save()
        return redirect('/create/manage/')

    denyMembershipForm = DenyMembershipForm(request.POST)
    if denyMembershipForm.is_valid():
        # Discard the membership
        Membership.objects.get(id=denyMembershipForm.cleaned_data['membershipIdToDeny']).delete()
        return redirect('/create/manage/')

    revokeMembershipForm = RevokeMembershipForm(request.POST)
    if revokeMembershipForm.is_valid():
        # Discard the membership
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
        organizationEditForm = OrganizationEditForm(request.POST)
        if organizationEditForm.is_valid():
            request.user.profile.organization.name = organizationEditForm.cleaned_data['name']
            request.user.profile.organization.private = organizationEditForm.cleaned_data['private']
            request.user.profile.organization.save()
        return redirect('/create/manage/')

    return render(request, 'edit_organization.html')
