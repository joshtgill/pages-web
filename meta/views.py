from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
import uuid
import django.contrib.auth as djangoAuth
from django.core.exceptions import ObjectDoesNotExist
from builder.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from builder.models import Organization, NewOrganizationRequest, Membership
from django.contrib.auth.decorators import login_required
from django.conf import settings


def home(request):
    return redirect('/profile/')


def createAccount(request):
    if request.method == 'GET':
        return render(request, 'create_account.html', {'createAccountForm': CreateAccountForm()})

    createAccountForm = CreateAccountForm(request.POST)
    if not createAccountForm.is_valid():
        return redirect('/create-account/')

    email = createAccountForm.cleaned_data['email']
    if User.objects.filter(email=email):
        return redirect('/create-account/')

    password = createAccountForm.cleaned_data['password']
    if password != createAccountForm.cleaned_data['repeatPassword']:
        return redirect('/create-account/')

    user = User.objects.create_user(uuid.uuid4(), email, password)
    user.first_name = createAccountForm.cleaned_data['firstName']
    user.last_name = createAccountForm.cleaned_data['lastName']
    user.save()
    profile = Profile()
    profile.user = user
    profile.save()

    djangoAuth.login(request, user)

    return redirect('/profile/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'loginForm': LoginForm()})

    loginForm = LoginForm(request.POST)
    if not loginForm.is_valid():
        return redirect('/login/')

    username = ''
    try:
        username = User.objects.get(email=loginForm.cleaned_data['email']).username
    except ObjectDoesNotExist:
        return redirect('/login/')

    loginUser = djangoAuth.authenticate(request, username=username, password=loginForm.cleaned_data['password'])
    if not loginUser:
        return redirect('/login/')

    djangoAuth.login(request, loginUser)

    return redirect('/profile/')


@login_required
def profile(request):
    if request.method == 'GET':
        content = {'memberships': Membership.objects.filter(user=request.user, approved=True)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'leaveOrganizationConfirmationPopupData': {'prompt': None,
                                                              'confirmButtonText': 'Leave',
                                                              'formName': 'membershipIdToEnd',
                                                              'formValue': None,
                                                              'dismissButtonText': 'Cancel'},
                   'changeEmailForm': ChangeEmailForm(),
                   'logoutPopupData': {'prompt': 'Logout of <b>{}</b>?'.format(request.user.email),
                                       'confirmButtonText': 'Logout',
                                       'formName': 'logout',
                                       'formValue': True,
                                       'dismissButtonText': 'Back'},
                   'deleteAccountPopupData': {'prompt': '''This will permanently delete the account associated
                                                           with <br><br><b>{}</b><br><br> All data will be lost
                                                           and this action cannot be undone.'''.format(request.user.email),
                                              'confirmButtonText': 'Delete',
                                              'formName': 'deleteAccount',
                                              'formValue': True,
                                              'dismissButtonText': 'Back'}}

        return render(request, 'profile.html', content)

    changeEmailForm = ChangeEmailForm(request.POST)
    if changeEmailForm.is_valid():
        newEmail = changeEmailForm.cleaned_data['newEmail']
        newEmailConfirm = changeEmailForm.cleaned_data['newEmailConfirm']
        if newEmail == newEmailConfirm:
            request.user.email = newEmail
            request.user.save()
        return redirect('/profile/')

    endMembershipForm = EndMembershipForm(request.POST)
    if endMembershipForm.is_valid():
        Membership.objects.get(id=endMembershipForm.cleaned_data['membershipIdToEnd']).delete()
        return redirect('/profile/')

    logoutForm = LogoutForm(request.POST)
    if logoutForm.is_valid():
        djangoAuth.logout(request)
        return redirect('/login/')

    deleteAccountForm = DeleteAccountForm(request.POST)
    if deleteAccountForm.is_valid():
        deleteUsername = request.user.username
        djangoAuth.logout(request)
        User.objects.get(username=deleteUsername).delete()
        return redirect('/login/')

    return redirect('/profile/')


@staff_member_required
def staff(request):
    organizations = Organization.objects.all()
    content = {'organizations': organizations[:settings.MAX_DASHBOARD_LIST_ENTRIES]}

    if request.method == 'GET':
        content.update({'newOrganizationRequests': NewOrganizationRequest.objects.all()[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                        'newOrganizationRequestApproveConfirmationPopupData': {'prompt': None,
                                                                               'confirmButtonText': 'Approve',
                                                                               'formName': 'newOrganizationRequestIdToApprove',
                                                                               'formValue': None,
                                                                               'dismissButtonText': 'Cancel'},
                        'newOrganizationRequestDenyConfirmationPopupData': {'prompt': None,
                                                                            'confirmButtonText': 'Deny',
                                                                            'formName': 'newOrganizationRequestIdToDeny',
                                                                            'formValue': None,
                                                                            'dismissButtonText': 'Cancel'},
                        'organizationDeleteConfirmationPopupData': {'prompt': None,
                                                                    'confirmButtonText': 'Delete',
                                                                    'formName': 'organizationIdToDelete',
                                                                    'formValue': None, # Will be overriden in template
                                                                    'dismissButtonText': 'Cancel'}})
        return render(request, 'staff.html', content)

    deleteOrganizationForm = DeleteOrganizationForm(request.POST)
    if deleteOrganizationForm.is_valid():
        organizations.get(id=deleteOrganizationForm.cleaned_data['organizationIdToDelete']).delete()
        return redirect('/staff/')

    approveNewOrganizationRequestForm = ApproveNewOrganizationRequestForm(request.POST)
    if approveNewOrganizationRequestForm.is_valid():
        newOrganizationRequest = NewOrganizationRequest.objects.get(id=approveNewOrganizationRequestForm.cleaned_data['newOrganizationRequestIdToApprove'])

        # Create organization
        organization = Organization(name=newOrganizationRequest.name, owner=newOrganizationRequest.applicant)
        organization.save()
        # Assign organization to user
        newOrganizationRequest.applicant.profile.organization = organization
        newOrganizationRequest.applicant.profile.save()
        # Delete organization request
        newOrganizationRequest.delete()

    denyNewOrganizationRequestForm = DenyNewOrganizationRequestForm(request.POST)
    if denyNewOrganizationRequestForm.is_valid():
        newOrganizationRequest = NewOrganizationRequest.objects.get(id=denyNewOrganizationRequestForm.cleaned_data['newOrganizationRequestIdToDeny'])

        # Delete organization request
        newOrganizationRequest.delete()

    return redirect('/staff/')
