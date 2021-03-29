from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization, Page, SheetItem, Event, Membership
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required


def explore(request):
    if request.method == 'GET':
        pageForm = PageForm(request.GET)
        if pageForm.is_valid():
            # Render the organization's Page.
            return render(request, 'view_page.html', {'pageData': buildPageData(pageForm.cleaned_data['page'])})

        organizationForm = OrganizationForm(request.GET)
        if organizationForm.is_valid():
            organization = None
            try:
                organization = Organization.objects.get(name__iexact=organizationForm.cleaned_data['organization'])
            except ObjectDoesNotExist:
                return redirect('/explore/')

            membershipRequestForm = MembershipRequestForm(request.POST)
            if membershipRequestForm.is_valid():
                # Membership request was submitted. Record it.
                membership = Membership(user=request.user, organization=organization, relatedDate=datetime.date.today())
                membership.save()
                return redirect('/profile/')

            content = {}
            if organization.private and not Membership.objects.filter(user=request.user,
                                                                    organization=organization,
                                                                    approved=True).count():
                # Organization is private and a membership does not exists with the user. Show membership request prompt.
                content.update({'requestMembershipData': {'prompt': '''{} requires approval to view its Pages.
                                                                    <br><br>Would you like to request approval?'''.format(organization.name),
                                                        'confirmButtonText': 'Request',
                                                        'formName': 'membershipRequest',
                                                        'formValue': True,
                                                        'dismissButtonText': 'Back'}})
            else:
                # Organization is viewable. Display its pages.
                content.update({'organization': organization, 'pagesData': buildOrganizationPagesData(organization)})

            return render(request, 'view_organization.html', content)

        # Neither forms were submitted, render organization search page
        return render(request, 'explore.html', {'organizationForm': OrganizationForm()})

    eventAttendanceForm = EventAttendanceForm(request.POST)
    if not eventAttendanceForm.is_valid():
        return redirect('/profile/')

    event = Event.objects.get(id=eventAttendanceForm.cleaned_data['eventId'])

    event.acceptees.remove(request.user)
    event.declinees.remove(request.user)

    if eventAttendanceForm.cleaned_data['status']:
        event.acceptees.add(request.user)
    else:
        event.declinees.add(request.user)

    event.save()

    return redirect('/profile/')


def buildPageData(pageId):
    page = Page.objects.get(id=pageId)
    pageData = {'name': page.name, 'type': page.typee, 'organization': page.organization}
    if page.typee == 'Sheet':
        pageData.update({'sheetItems': SheetItem.objects.filter(page=page)})
    elif page.typee == 'Event':
        pageData.update({'event': Event.objects.get(page=page)})

    return pageData


def buildOrganizationPagesData(organization):
    organizationPagesData = []
    for page in Page.objects.filter(organization=organization):
        organizationPagesData.append({'id': page.id, 'name': page.name})

    return organizationPagesData
