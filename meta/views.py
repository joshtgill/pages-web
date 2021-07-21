from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
import uuid
import django.contrib.auth as djangoAuth
from django.core.exceptions import ObjectDoesNotExist
from builder.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from builder.models import Organization, Membership
from django.contrib.auth.decorators import login_required
from django.conf import settings
import datetime


def home(request):
    return redirect('/profile/')


def createAccount(request):
    content = {'createAccountForm': CreateAccountForm()}

    if request.method == 'GET':
        return render(request, 'create_account.html', content)

    createAccountForm = CreateAccountForm(request.POST)
    if not createAccountForm.is_valid():
        return redirect('/create-account/')

    user = User()
    error = user.create(request,
                        createAccountForm.cleaned_data['email'],
                        createAccountForm.cleaned_data['password'],
                        createAccountForm.cleaned_data['repeatPassword'],
                        createAccountForm.cleaned_data['firstName'],
                        createAccountForm.cleaned_data['lastName'])
    if error:
        content.update({'error': error})
        return render(request, 'create_account.html', content)

    return redirect('/profile/')


def login(request):
    content = {'loginForm': LoginForm()}

    if request.method == 'GET':
        return render(request, 'login.html', content)

    loginForm = LoginForm(request.POST)
    if not loginForm.is_valid():
        return redirect('/login/')

    error = User().login(request, loginForm.cleaned_data['email'], loginForm.cleaned_data['password'])
    if error:
        print(error)
        content.update({'error': error})
        return render(request, 'login.html', content)

    return redirect('/profile/')


@login_required
def profile(request):
    content = {'pendingMemberships': Membership.objects.filter(user=request.user, approved=False),
               'memberships': Membership.objects.filter(user=request.user, approved=True),
               'changeEmailForm': ChangeEmailForm()}

    if request.method == 'GET':
        return render(request, 'profile.html', content)

    changeEmailForm = ChangeEmailForm(request.POST)
    if changeEmailForm.is_valid():
        error = request.user.changeEmail(changeEmailForm.cleaned_data['newEmail'], changeEmailForm.cleaned_data['newEmailConfirm'])
        if error:
            content.update({'error': error})
        return render(request, 'profile.html', content)

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
    content = {'organizations': Organization.objects.all()}

    if request.method == 'GET':
        content.update({'unapprovedOrganizations': Organization.objects.filter(approved=False)})
        return render(request, 'staff.html', content)

    deleteOrganizationForm = DeleteOrganizationForm(request.POST)
    if deleteOrganizationForm.is_valid():
        Organization.objects.all().get(id=deleteOrganizationForm.cleaned_data['organizationIdToDelete']).delete()
        return redirect('/staff/')

    approveOrganizationForm = ApproveOrganizationForm(request.POST)
    if approveOrganizationForm.is_valid():
        Organization.objects.get(id=approveOrganizationForm.cleaned_data['organizationIdToApprove']).approve()

    denyOrganizationForm = DenyOrganizationForm(request.POST)
    if denyOrganizationForm.is_valid():
        Organization.objects.get(id=denyOrganizationForm.cleaned_data['organizationIdToDeny']).delete()

    return redirect('/staff/')
