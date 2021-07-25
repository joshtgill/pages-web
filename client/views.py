from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization, Page, SheetItem, EventItem, Membership, SingleOccurence, RepeatingOccurence
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


def explore(request):
    if request.method == 'GET':
        pageForm = PageForm(request.GET)
        if pageForm.is_valid():
            # Render the organization's Page.
            return render(request, 'view_page.html', {'organizationName': pageForm.cleaned_data['organization'],
                                                      'pageData': Page.objects.get(id=pageForm.cleaned_data['page']).serialize()})

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
                content.update({'pages': Page.objects.filter(organization=organization)})

            return render(request, 'view_organization.html', content)

        # Neither forms were submitted, render organization search page
        return render(request, 'explore.html', {'organizationForm': OrganizationForm()})

    requestMembershipForm = RequestMembershipForm(request.POST)
    if requestMembershipForm.is_valid():
        # Create a membership request
        Membership.objects.create(Organization.objects.get(id=requestMembershipForm.cleaned_data['organizationIdToRequestMembership']),
                                  request.user,
                                  False)
        return redirect('/profile/')

    eventAttendanceForm = EventAttendanceForm(request.POST)
    if not eventAttendanceForm.is_valid():
        return redirect('/profile/')

    eventItem = EventItem.objects.get(id=eventAttendanceForm.cleaned_data['eventId'])
    eventItem.updateAttendance(request.user, eventAttendanceForm.cleaned_data['status'])

    return redirect('/explore/?organization={}&page={}'.format(eventItem.page.organization.name, eventItem.page.id))
