from .models import *
from django.shortcuts import render, redirect
from .forms import *


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

        pageForm = PageForm(request.GET)
        if not pageForm.is_valid():
            return render(request, 'builder.html', {'pages': pages})

        return render(request, 'page.html', {'page': pages.get(name=pageForm.cleaned_data['name'])})

    sheetsPostData = dict(request.POST)

    name = sheetsPostData.get('name')[0]
    sheet = Sheet(name=name)
    sheet.organization = request.user.creatoruser.organization
    sheet.save()

    itemTitles = sheetsPostData.get('title')
    itemDescriptions = sheetsPostData.get('description')
    itemPrices = sheetsPostData.get('price')
    for i in range(len(itemTitles)):
        sheetItem = SheetItem(title=itemTitles[i], description=itemDescriptions[i], price=itemPrices[i])
        sheetItem.sheet = sheet
        sheetItem.save()

    return redirect('/create/')
