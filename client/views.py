from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization, Page, SheetItem, Membership
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required


def explore(request):
    organizationForm = OrganizationForm(request.GET)
    pageForm = PageForm(request.GET)

    if pageForm.is_valid():
        # Render the Page page.
        return render(request, 'view_page.html', {'pageData': buildPageData(pageForm.cleaned_data['page'])})
    elif organizationForm.is_valid():
        # If the organization exists, navigate to its page. Otherwise return to organization search page.
        organization = None
        try:
            organization = Organization.objects.get(name__iexact=organizationForm.cleaned_data['organization'])
        except ObjectDoesNotExist:
            return redirect('/explore/')

        requestApprovalForm = RequestApprovalForm(request.POST)
        if requestApprovalForm.is_valid():
            # Submit approval
            membership = Membership(user=request.user, organization=organization, relatedDate=datetime.date.today())
            membership.save()
            return redirect('/profile/')

        content = {'organization': organization, 'pagesData': buildOrganizationPagesData(organization)}
        if organization.private and not Membership.objects.filter(user=request.user, organization=organization, approved=True).count():
            content.update({'requestApprovalData': {'prompt': '''{} requires approval to view its Pages.
                                                                 <br><br>Would you like to request approval?'''.format(organization.name),
                                                    'confirmButtonText': 'Request',
                                                    'formName': 'requestApproval',
                                                    'formValue': True,
                                                    'dismissButtonText': 'Back'}})

        return render(request, 'view_organization.html', content)

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
