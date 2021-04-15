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
import datetime


def home(request):
    return redirect('/profile/')


def createAccount(request):
    if request.method == 'GET':
        return render(request, 'create_account.html', {'createAccountForm': CreateAccountForm()})

    createAccountForm = CreateAccountForm(request.POST)
    if not createAccountForm.is_valid():
        return redirect('/create-account/')

    user = User()
    isSuccesful = user.create(request,
                              createAccountForm.cleaned_data['email'],
                              createAccountForm.cleaned_data['password'],
                              createAccountForm.cleaned_data['repeatPassword'],
                              createAccountForm.cleaned_data['firstName'],
                              createAccountForm.cleaned_data['lastName'])
    if not isSuccesful:
        return redirect('/create-account/')

    return redirect('/profile/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'loginForm': LoginForm()})

    loginForm = LoginForm(request.POST)
    if not loginForm.is_valid():
        return redirect('/login/')

    isSuccessful = User().login(request, loginForm.cleaned_data['email'], loginForm.cleaned_data['password'])
    if not isSuccessful:
        return redirect('/login/')

    return redirect('/profile/')


@login_required
def profile(request):
    if request.method == 'GET':
        content = {'pendingMemberships': Membership.objects.filter(user=request.user, approved=False)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'memberships': Membership.objects.filter(user=request.user, approved=True)[:settings.MAX_DASHBOARD_LIST_ENTRIES],
                   'changeEmailForm': ChangeEmailForm()}

        return render(request, 'profile.html', content)

    changeEmailForm = ChangeEmailForm(request.POST)
    if changeEmailForm.is_valid():
        request.user.changeEmail(changeEmailForm.cleaned_data['newEmail'], changeEmailForm.cleaned_data['newEmailConfirm'])
        return redirect('/profile/')

    cancelMembershipForm = CancelMembershipForm(request.POST)
    if cancelMembershipForm.is_valid():
        Membership.objects.get(id=cancelMembershipForm.cleaned_data['membershipIdToCancel']).delete()
        return redirect('/profile/')

    logoutForm = LogoutForm(request.POST)
    if logoutForm.is_valid():
        djangoAuth.logout(request)
        return redirect('/login/')

    deleteAccountForm = DeleteAccountForm(request.POST)
    if deleteAccountForm.is_valid():
        request.user.deletee(request)
        return redirect('/login/')

    return redirect('/profile/')


@staff_member_required
def staff(request):
    content = {'organizations': Organization.objects.all()[:settings.MAX_DASHBOARD_LIST_ENTRIES]}

    if request.method == 'GET':
        content.update({'newOrganizationRequests': NewOrganizationRequest.objects.all()[:settings.MAX_DASHBOARD_LIST_ENTRIES]})
        return render(request, 'staff.html', content)

    deleteOrganizationForm = DeleteOrganizationForm(request.POST)
    if deleteOrganizationForm.is_valid():
        Organization.objects.all().get(id=deleteOrganizationForm.cleaned_data['organizationIdToDelete']).delete()
        return redirect('/staff/')

    approveNewOrganizationRequestForm = ApproveNewOrganizationRequestForm(request.POST)
    if approveNewOrganizationRequestForm.is_valid():
        Organization().create(NewOrganizationRequest.objects.get(id=approveNewOrganizationRequestForm.cleaned_data['newOrganizationRequestIdToApprove']))

    denyNewOrganizationRequestForm = DenyNewOrganizationRequestForm(request.POST)
    if denyNewOrganizationRequestForm.is_valid():
        NewOrganizationRequest.objects.get(id=denyNewOrganizationRequestForm.cleaned_data['newOrganizationRequestIdToDeny']).delete()

    return redirect('/staff/')
