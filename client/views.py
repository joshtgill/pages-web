from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization, Page, SheetItem
from django.core.exceptions import ObjectDoesNotExist


def explore(request):
    organizationForm = OrganizationForm(request.GET)
    pageForm = PageForm(request.GET)

    if pageForm.is_valid():
        # On valid Page Form, render Page page.
        return render(request, 'view_page.html', {'pageData': buildPageData(pageForm.cleaned_data['page'])})
    elif organizationForm.is_valid():
        # On valid Organization Form, show organization's Pages if the organization exists.
        # Otherwise, go to the organization search page
        organiation = None
        try:
            organization = Organization.objects.get(name__iexact=organizationForm.cleaned_data['organization'])
        except ObjectDoesNotExist:
            return redirect('/explore/')

        return render(request, 'view_organization.html', {'organization': organization,
                                                          'pagesData': buildOrganizationPagesData(organization)})

    # Neither forms were submitted, render organization search page
    return render(request, 'explore.html', {'organizationForm': OrganizationForm()})


def buildPageData(pageId):
    page = Page.objects.get(id=pageId)
    pageData = {'name': page.name, 'sheetItems': SheetItem.objects.filter(page=page)}

    return pageData


def buildOrganizationPagesData(organization):
    organizationPagesData = []
    for page in Page.objects.filter(organization=organization):
        organizationPagesData.append({'id': page.id, 'name': page.name})

    return organizationPagesData
