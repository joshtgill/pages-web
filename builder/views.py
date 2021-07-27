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

    Membership().create(Organization.objects.get(id=selectOrganizationForm.cleaned_data['ids']), request.user, True)

    return redirect('/create/')


@login_required
def registerOrganization(request):
    if request.method == 'GET':
        return render(request, 'register_organization.html', {'registerOrganizationForm': RegisterOrganizationForm()})

    registerOrganizationForm = RegisterOrganizationForm(request.POST)
    if not registerOrganizationForm.is_valid():
        return redirect('/create/register/')

    Organization.objects.create(registerOrganizationForm.cleaned_data['name'],
                                registerOrganizationForm.cleaned_data['headquarters'],
                                registerOrganizationForm.cleaned_data['description'],
                                request.user)

    return redirect('/profile/')


@login_required
def build(request):
    if request.method == 'GET':
        buildForm = BuildForm(request.GET)

        if not buildForm.is_valid():
            # Page type isn't provided, list available Pages
            return render(request, 'select_page_type.html', {'pageInfos': PageInfo.objects.all()})

        pageInfo = PageInfo.objects.get(type=buildForm.cleaned_data['type'])
        if not pageInfo:
            return redirect('/create/build/')

        content = {'defaultExplanation': pageInfo.defaultExplanation, 'pageInfos': PageInfo.objects.all() }
        pageId = buildForm.cleaned_data['idd']
        if pageId and Page.objects.filter(organization=request.user.profile.organization, id=pageId).exists():
            # Page ID is provided and belongs to active organization. Load Page builder with existing data.
            content.update({'pageData': Page.objects.get(id=pageId).serialize()})
        else:
            # Invalid Page ID is provided with respect to organization. Load empty Page builder.
            content.update({'pageData': {'info': pageInfo, 'items': {}}})

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

    return redirect('/create/manage/')


@login_required
def manageOrganization(request):
    if request.method == 'GET':
        content = {'activePagesData': request.user.profile.organization.getPagesData(),
                   'memberRequests': Membership.objects.filter(approved=False),
                   'organizationMembers': Membership.objects.filter(organization=request.user.profile.organization, approved=True)}
        return render(request, 'manage_organization.html', content)

    deletePageForm = DeletePageForm(request.POST)
    if deletePageForm.is_valid():
        Page.objects.get(id=deletePageForm.cleaned_data['pageIdToDelete']).delete()
        return redirect('/create/manage/')

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
        Membership.objects.get(id=approveMembershipForm.cleaned_data['membershipIdToApprove']).approve()
        return redirect('/create/manage/')

    denyMembershipForm = DenyMembershipForm(request.POST)
    if denyMembershipForm.is_valid():
        Membership.objects.get(id=denyMembershipForm.cleaned_data['membershipIdToDeny']).delete()
        return redirect('/create/manage/')

    revokeMembershipForm = RevokeMembershipForm(request.POST)
    if revokeMembershipForm.is_valid():
        Membership.objects.get(id=revokeMembershipForm.cleaned_data['membershipIdToRevoke']).delete()

    return redirect('/create/manage/')


@login_required
def editOrganization(request):
    if request.method == 'POST':
        editOrganizationForm = EditOrganizationForm(request.POST)
        if editOrganizationForm.is_valid():
            request.user.profile.organization.deserialize(editOrganizationForm.cleaned_data)
        return redirect('/create/manage/')

    return render(request, 'edit_organization.html')
