from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization, Page, SheetItem, Event, Membership, SingleOccurence, RepeatingOccurence
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


def explore(request):
    if request.method == 'GET':
        pageForm = PageForm(request.GET)
        if pageForm.is_valid():
            # Render the organization's Page.
            return render(request, 'view_page.html', {'pageData': Page.objects.get(id=pageForm.cleaned_data['page']).serialize()})

        organizationForm = OrganizationForm(request.GET)
        if organizationForm.is_valid():
            organization = None
            try:
                organization = Organization.objects.get(name__iexact=organizationForm.cleaned_data['organization'])
            except ObjectDoesNotExist:
                return redirect('/explore/')

            content = {'organization': organization}
            if not organization.isPrivate or Membership.objects.filter(user=request.user,
                                                                       organization=organization,
                                                                       approved=True).count():
                # Organization is viewable. Display its pages.
                content.update({'pagesData': buildOrganizationPagesData(organization)})

            return render(request, 'view_organization.html', content)

        # Neither forms were submitted, render organization search page
        return render(request, 'explore.html', {'organizationForm': OrganizationForm()})

    requestMembershipForm = RequestMembershipForm(request.POST)
    if requestMembershipForm.is_valid():
        # Membership request was submitted. Record it.
        membership = Membership(user=request.user,
                                organization=Organization.objects.get(id=requestMembershipForm.cleaned_data['organizationIdToRequestMembership']),
                                relatedDate=datetime.date.today())
        membership.save()
        return redirect('/profile/')

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

    return redirect('/explore/?organization={}&page={}'.format(event.page.organization.name, event.page.id))


def buildOrganizationPagesData(organization):
    organizationPagesData = []
    for page in Page.objects.filter(organization=organization):
        organizationPagesData.append({'id': page.id, 'name': page.name})

    return organizationPagesData
