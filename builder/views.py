from .models import *
from django.shortcuts import render, redirect
from .forms import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


def createPitch(request):
    return render(request, 'create_pitch.html')


@login_required
def selectOrganization(request):
    organizations = Organization.objects.all()
    content = {'selectOrganizationForm': SelectOrganizationForm(organizations=organizations)}
    if request.method == 'GET':
        return render(request, 'select_organization.html', content)

    selectOrganizationForm = SelectOrganizationForm(request.POST, organizations=organizations)
    if not selectOrganizationForm.is_valid():
        return redirect('/create/select/')

    organization = Organization.objects.get(id=selectOrganizationForm.cleaned_data['ids'])
    request.user.profile.organization = organization
    if not Membership.objects.filter(user=request.user, organization=organization).exists():
        membership = Membership(user=request.user, organization=organization, relatedDate=datetime.date.today(), approved=True)
        membership.save()

    request.user.profile.save()

    return redirect('/create/')


@login_required
def requestNewOrganization(request):
    if request.method == 'GET':
        return render(request, 'request_new_organization.html', {'requestNewOrganizationForm': RequestNewOrganizationForm()})

    requestNewOrganizationForm = RequestNewOrganizationForm(request.POST)
    if not requestNewOrganizationForm.is_valid():
        return redirect('/create/request/')

    newOrganizationRequest = NewOrganizationRequest(name=requestNewOrganizationForm.cleaned_data['name'])
    newOrganizationRequest.applicant = request.user
    newOrganizationRequest.save()

    return redirect('/profile/')


@login_required
def build(request):
    if request.method == 'GET':
        buildForm = BuildForm(request.GET)

        if not buildForm.is_valid():
            # Page type isn't provided, list available Pages
            return render(request, 'select_page_type.html', {'pageListings': PageListing.objects.all()})

        pageType = buildForm.cleaned_data['typee']
        if not PageListing.objects.filter(name=pageType).exists():
            return redirect('/create/build/')

        content = {}
        pageId = buildForm.cleaned_data['idd']
        if pageId and Page.objects.filter(organization=request.user.profile.organization, id=pageId).exists():
            # Page ID is provided and belongs to active organization. Load Page builder with existing data.
            pageData = Page.objects.get(id=pageId).serialize()
            content.update({'pageData': pageData})
        else:
            # Invalid Page ID is provided with respect to organization. Load empty Page builder.
            content.update({'pageData': {'typee': pageType}})

        return render(request, 'build_page.html', content)

    deletePageForm = DeletePageForm(request.POST)
    if deletePageForm.is_valid():
        Page.objects.get(id=deletePageForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/manage/')

    # Send post data to handle Page updates
    pagePostData = dict(request.POST)
    page = None
    try:
        page = Page.objects.get(id=pagePostData.get('pageId')[0])
    except ValueError:
        page = Page(organization=request.user.profile.organization)
    page.deserialize(pagePostData)
    page.save()

    return redirect('/create/manage/')


@login_required
def manageOrganization(request):
    if request.method == 'GET':
        content = {'numOrganizationsMemberships': len(Membership.objects.filter(organization=request.user.profile.organization, approved=True)),
                   'activePagesData': buildOrganizationsPagesData(request.user.profile.organization),
                   'memberRequests': Membership.objects.filter(approved=False)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'organizationMembers': Membership.objects.filter(organization=request.user.profile.organization, approved=True)[:settings.MAX_DASHBOARD_LIST_ENTRIES]}
        return render(request, 'manage_organization.html', content)

    leaveOrganizationForm = LeaveOrganizationForm(request.POST)
    if leaveOrganizationForm.is_valid() and request.user.profile.organization.owner != request.user:
        request.user.profile.organization = None
        request.user.profile.save()
        return redirect('/')

    deleteOrganizationForm = DeleteOrganizationForm(request.POST)
    if deleteOrganizationForm.is_valid():
        request.user.profile.organization.delete()
        return redirect('/')

    approveMembershipForm = ApproveMembershipForm(request.POST)
    if approveMembershipForm.is_valid():
        membership = Membership.objects.get(id=approveMembershipForm.cleaned_data['membershipIdToApprove'])
        membership.relatedDate = datetime.date.today()
        membership.approved = True
        membership.save()
        return redirect('/create/manage/')

    denyMembershipForm = DenyMembershipForm(request.POST)
    if denyMembershipForm.is_valid():
        Membership.objects.get(id=denyMembershipForm.cleaned_data['membershipIdToDeny']).delete()
        return redirect('/create/manage/')

    revokeMembershipForm = RevokeMembershipForm(request.POST)
    if revokeMembershipForm.is_valid():
        Membership.objects.get(id=revokeMembershipForm.cleaned_data['membershipIdToRevoke']).delete()

    return redirect('/create/manage/')


def buildOrganizationsPagesData(organization):
    organizationsPagesData = []
    for page in Page.objects.filter(organization=organization)[:settings.MAX_DASHBOARD_LIST_ENTRIES]:
        organizationsPagesData.append(page.serialize(False))

    return organizationsPagesData


@login_required
def editOrganization(request):
    if request.method == 'POST':
        editOrganizationForm = EditOrganizationForm(request.POST)
        if editOrganizationForm.is_valid():
            request.user.profile.organization.deserialize(editOrganizationForm.cleaned_data)
            request.user.profile.organization.save()
        return redirect('/create/manage/')

    return render(request, 'edit_organization.html')
