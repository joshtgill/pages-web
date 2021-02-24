from .models import *
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.core.exceptions import ObjectDoesNotExist


def creatorUpgrade(request):
    organizations = Organization.objects.all()
    content = {'organizationForm': OrganizationForm(organizations=organizations)}

    if request.method == 'GET':
        return render(request, 'creator_upgrade.html', content)

    submittedOrganizationForm = OrganizationForm(request.POST, organizations=organizations)
    if not submittedOrganizationForm.is_valid():
        return render(request, 'creator_upgrade.html', content)

    creatorUser = CreatorUser()
    creatorUser.user = request.user
    creatorUser.organization = Organization.objects.get(id=submittedOrganizationForm.cleaned_data['names'])
    creatorUser.save()

    return redirect('/profile/')


def create(request):
    return render(request, 'create.html')


def builder(request):
    if request.method == 'GET':
        pageListings = PageListing.objects.all()

        builderForm = BuilderForm(request.GET)
        if not builderForm.is_valid():
            return render(request, 'builder.html', {'pageListings': pageListings})

        content = {'pageType': builderForm.cleaned_data['typee']}

        pageId = builderForm.cleaned_data['idd']
        if pageId:
            pageData = buildPageData(pageId)
            content.update({'pageData': pageData,
                            'pageDeletePopupData': {'prompt': 'Permanently delete <b>{}</b> from {}?'.format(pageData.get('name'),
                                                                                                             request.user.creatoruser.organization.name),
                                                    'confirmButtonText': 'Delete',
                                                    'formName': 'pageIdToDelete',
                                                    'formValue': pageData.get('id')}})

        return render(request, 'page.html', content)

    pageDeleteForm = PageDeleteForm(request.POST)
    if pageDeleteForm.is_valid():
        Page.objects.get(id=pageDeleteForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/pages/')

    pagePostData = dict(request.POST)
    page = handlePageUpdate(request, pagePostData)
    handleSheetItemsUpdates(pagePostData, page)

    return redirect('/create/pages/')


def handlePageUpdate(request, pagePostData):
    # If the Page exists, update its name. Otherwise create it.
    page = None
    try:
        page = Page.objects.get(id=pagePostData.get('pageId')[0])
        page.name = pagePostData.get('pageName')[0]
    except ValueError:
        page = Page(name=pagePostData.get('pageName')[0], dateCreated=datetime.date.today())
        page.organization = request.user.creatoruser.organization
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


def buildPageData(idd):
    page = Page.objects.get(id=idd)
    return {'id': page.id, 'name': page.name, 'items': SheetItem.objects.filter(page=page)}


def pages(request):
    if request.method == 'GET':
        return render(request, 'pages.html', {'pagesData': buildPagesData(request)})

    builderForm = BuilderForm(request.POST)
    if not builderForm.is_valid():
        return render(request, 'home.html')

    pageId = builderForm.cleaned_data['name']

    return redirect('/create/builder/?name=Sheet?id={}'.format(pageId))


def buildPagesData(request):
    pagesData = []
    for page in Page.objects.filter(organization=request.user.creatoruser.organization):
        pagesData.append({'id': page.id, 'name': page.name, 'dateCreated': page.dateCreated,
                          'numItems': len(SheetItem.objects.filter(page=page))})

    return pagesData
