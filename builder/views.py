from .models import *
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.core.exceptions import ObjectDoesNotExist


def create(request):
    return render(request, 'create_pitch.html')


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
            content.update({'pageData': {'type': pageType}})

        return render(request, 'builder_page.html', content)

    pageDeleteForm = PageDeleteForm(request.POST)
    if pageDeleteForm.is_valid():
        Page.objects.get(id=pageDeleteForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/manage-organization/')

    pagePostData = dict(request.POST)
    page = handlePageUpdate(request, pagePostData)
    handleSheetItemsUpdates(pagePostData, page)

    return redirect('/create/manage-organization/')


def buildPageData(idd):
    page = Page.objects.get(id=idd)
    return {'id': page.id, 'name': page.name, 'type': page.typee, 'items': SheetItem.objects.filter(page=page)}


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
    # Delete appropiate Sheet Items
    try:
        for sheetItemId in pagePostData.get('pageItemIdsToDelete')[0].split('|'):
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
    for i in range(len(sheetItemIds)):
        try:
            sheetItem = SheetItem.objects.get(id=int(sheetItemIds[i]))
            sheetItem.title = sheetItemTitles[i]
            sheetItem.description = sheetItemDescriptions[i]
            sheetItem.price = sheetItemPrices[i]
        except ObjectDoesNotExist:
            sheetItem = SheetItem(title=sheetItemTitles[i], description=sheetItemDescriptions[i], price=sheetItemPrices[i])
            sheetItem.page = page
        sheetItem.save()


def manageOrganization(request):
    if request.method == 'GET':
        content = {'activePagesData': buildOrganizationsPagesData(request.user.profile.organization),
                   'leaveOrganizationConfirmationPopupData': {'prompt': 'Leave {}?'.format(request.user.profile.organization.name),
                                                              'confirmButtonText': 'Leave',
                                                              'formName': 'leaveOrganization',
                                                              'formValue': True,
                                                              'dismissButtonText': 'Cancel'}}
        return render(request, 'manage_organization.html', content)

    leaveOrganizationForm = LeaveOrganizationForm(request.POST)
    if not leaveOrganizationForm.is_valid():
        return redirect('/create/manage/')

    request.user.profile.organization = None
    request.user.profile.save()

    return redirect('/')


def buildOrganizationsPagesData(organization):
    organizationsPagesData = []
    for page in Page.objects.filter(organization=organization):
        organizationsPagesData.append({'id': page.id, 'name': page.name, 'type': page.typee,
                                       'dateCreated': page.dateCreated.strftime("%B %d, %Y"),
                                       'numItems': len(SheetItem.objects.filter(page=page))})

    return organizationsPagesData


def editOrganization(request):
    if request.method == 'POST':
        organizationEditForm = OrganizationEditForm(request.POST)
        if organizationEditForm.is_valid():
            request.user.profile.organization.name = organizationEditForm.cleaned_data['name']
            request.user.profile.organization.private = organizationEditForm.cleaned_data['private']
            request.user.profile.organization.save()
        return redirect('/create/manage/')

    return render(request, 'edit_organization.html')
