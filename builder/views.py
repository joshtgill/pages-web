from .models import *
from django.shortcuts import render, redirect
from .forms import *
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
        pages = Page.objects.all()

        builderForm = BuilderForm(request.GET)
        if not builderForm.is_valid():
            return render(request, 'builder.html', {'pages': pages})

        pageType = builderForm.cleaned_data['typee']
        sheetId = builderForm.cleaned_data['idd']
        if sheetId:
            return render(request, 'page.html', {'page': pages.get(name=pageType), 'sheetData': buildSheetData(sheetId)})
        else:
            return render(request, 'page.html', {'page': pages.get(name=pageType)})

    deleteSheetItemForm = DeleteSheetItemForm(request.POST)
    if deleteSheetItemForm.is_valid():
        sheetId = deleteSheetItemForm.cleaned_data['sheetId']
        sheetItemId = deleteSheetItemForm.cleaned_data['sheetItemId']
        if sheetItemId == -1:
            Sheet.objects.get(id=sheetId).delete()
            return redirect('/create/pages/')
        else:
            print(sheetItemId)
            SheetItem.objects.get(id=sheetItemId).delete()
            return redirect('/create/builder/?typee=Sheet&idd={}'.format(sheetId))

    sheetsPostData = dict(request.POST)

    sheet = None
    try:
        sheet = Sheet.objects.get(id=sheetsPostData.get('sheetId')[0])
        sheet.name = sheetsPostData.get('sheetName')[0]
    except ValueError:
        sheet = Sheet(name=sheetsPostData.get('sheetName')[0])
        sheet.organization = request.user.creatoruser.organization
    sheet.save()

    sheetItemIds = sheetsPostData.get('id')
    sheetItemTitles = sheetsPostData.get('title')
    sheetItemDescriptions = sheetsPostData.get('description')
    sheetItemPrices = sheetsPostData.get('price')
    for i in range(len(sheetItemTitles)):
        try:
            sheetItem = SheetItem.objects.get(id=int(sheetItemIds[i]))
            sheetItem.title = sheetItemTitles[i]
            sheetItem.description = sheetItemDescriptions[i]
            sheetItem.price = sheetItemPrices[i]
        except ObjectDoesNotExist:
            sheetItem = SheetItem(title=sheetItemTitles[i], description=sheetItemDescriptions[i], price=sheetItemPrices[i])
            sheetItem.sheet = sheet
        sheetItem.save()

    return redirect('/create/pages/')


def buildSheetData(idd):
    sheet = Sheet.objects.get(id=idd)
    sheetData = {'name': sheet.name, 'id': sheet.id, 'items': SheetItem.objects.filter(sheet=sheet)}

    return sheetData


def pages(request):
    if request.method == 'GET':
        return render(request, 'pages.html', {'sheets': Sheet.objects.filter(organization=request.user.creatoruser.organization.id)})

    builderForm = BuilderForm(request.POST)
    if not builderForm.is_valid():
        return render(request, 'home.html')

    sheetId = builderForm.cleaned_data['name']

    return redirect('/create/builder/?name=Sheet?id={}'.format(sheetId))
