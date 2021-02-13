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
    return render(request, 'builder.html', {'pageNames': [page.name for page in Page.objects.all()]})


def page(request):
    if request.method == 'GET':
        pageForm = PageForm(request.GET)
        if not pageForm.is_valid():
            render(request, 'page.html')

        page = Page.objects.get(name=pageForm.cleaned_data['name'])

        return render(request, 'page.html', {'page': page})

    return render(request, 'page.html')
