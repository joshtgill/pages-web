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

    return redirect('/explore/?organization={}&page={}'.format(event.page.organization.name, event.page.id))


def buildPageData(pageId):
    page = Page.objects.get(id=pageId)
    pageData = {'id': page.id, 'name': page.name, 'type': page.typee, 'organization': page.organization}
    if page.typee == 'Sheet':
        sheetItemsData = []
        for sheetItem in SheetItem.objects.filter(page=page):
            sheetItemData = model_to_dict(sheetItem)
            if SingleOccurence.objects.filter(sheetItem=sheetItem).exists():
                sheetItemData.update({'singleOccurence': model_to_dict(SingleOccurence.objects.get(sheetItem=sheetItem))})
            elif RepeatingOccurence.objects.filter(sheetItem=sheetItem).exists():
                sheetItemData.update({'repeatingOccurence': model_to_dict(RepeatingOccurence.objects.get(sheetItem=sheetItem))})
            sheetItemsData.append(sheetItemData)
        pageData.update({'sheetItems': sheetItemsData})
    elif page.typee == 'Event':
        event = Event.objects.get(page=page)
        eventData = model_to_dict(event)
        if SingleOccurence.objects.filter(event=event).exists():
            eventData.update({'singleOccurence': model_to_dict(SingleOccurence.objects.get(event=event))})
        elif RepeatingOccurence.objects.filter(event=event).exists():
            eventData.update({'repeatingOccurence': model_to_dict(RepeatingOccurence.objects.get(event=event))})
        pageData.update({'event': eventData})

    return pageData


def buildOrganizationPagesData(organization):
    organizationPagesData = []
    for page in Page.objects.filter(organization=organization):
        organizationPagesData.append({'id': page.id, 'name': page.name})

    return organizationPagesData
