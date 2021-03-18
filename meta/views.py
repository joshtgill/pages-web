from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
import uuid
import django.contrib.auth as djangoAuth
from django.core.exceptions import ObjectDoesNotExist
from builder.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from builder.models import Organization, OrganizationApplication, Membership
from django.contrib.auth.decorators import login_required


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'memberships': Membership.objects.filter(user=request.user, approved=True),
                                             'leaveOrganizationConfirmationPopupData': {'prompt': None,
                                                                                        'confirmButtonText': 'Leave',
                                                                                        'formName': 'membershipIdToEnd',
                                                                                        'formValue': None,
                                                                                        'dismissButtonText': 'Cancel'}})

    endMembershipForm = EndMembershipForm(request.POST)
    if not endMembershipForm.is_valid():
        return redirect('/')

    Membership.objects.get(id=endMembershipForm.cleaned_data['membershipIdToEnd']).delete()

    return redirect('/')


def createAccount(request):
    emptyCreateAccountForm = CreateAccountForm()

    if request.method == 'GET':
        return render(request, 'create_account.html', {'createAccountForm': emptyCreateAccountForm})

    submittedCreateAccountForm = CreateAccountForm(request.POST)
    if not submittedCreateAccountForm.is_valid():
        return render(request, 'create_account.html', {'createAccountForm': emptyCreateAccountForm})

    # Verify that form email is not already registered
    email = submittedCreateAccountForm.cleaned_data['email']
    if User.objects.filter(email=email):
        return render(request, 'create_account.html', {'createAccountForm': submittedCreateAccountForm,
                                                       'errorInfo': {'message': 'Account already exists.',
                                                                     'linkText': 'Login',
                                                                     'linkAddress': 'login'}})

    # Verify that form passwords match
    password = submittedCreateAccountForm.cleaned_data['password']
    if password != submittedCreateAccountForm.cleaned_data['repeatPassword']:
        return render(request, 'create_account.html', {'createAccountForm': submittedCreateAccountForm,
                                                       'errorInfo': {'message': 'Passwords did not match. Try again.'}})

    createUser = User.objects.create_user(uuid.uuid4(), email, password)
    createUser.first_name = submittedCreateAccountForm.cleaned_data['firstName']
    createUser.last_name = submittedCreateAccountForm.cleaned_data['lastName']
    createUser.save()
    profile = Profile()
    profile.user = createUser
    profile.save()

    djangoAuth.login(request, createUser)

    return redirect('/profile/')


def login(request):
    emptyLoginForm = LoginForm()

    if request.method == 'GET':
        return render(request, 'login.html', {'loginForm': emptyLoginForm})

    submittedLoginForm = LoginForm(request.POST)
    if not submittedLoginForm.is_valid():
        return render(request, 'login.html', {'loginForm': emptyLoginForm})

    # Attempt to get username by form email
    username = ''
    try:
        username = User.objects.get(email=submittedLoginForm.cleaned_data['email']).username
    except ObjectDoesNotExist:
        return render(request, 'login.html', {'loginForm': emptyLoginForm, 'errorInfo': {'message': 'Account not found.',
                                                                                         'linkText': 'Create an account',
                                                                                         'linkAddress': 'create_account'}})

    # Attempt to authenticate username and password
    loginUser = djangoAuth.authenticate(request, username=username, password=submittedLoginForm.cleaned_data['password'])
    if not loginUser:
        return render(request, 'login.html', {'loginForm': submittedLoginForm, 'errorInfo': {'message': 'Incorrect password.',
                                                                                             'linkText': 'Reset password',
                                                                                             'linkAddress': 'home'}})

    djangoAuth.login(request, loginUser)

    return redirect('/profile/')


@login_required
def profile(request):
    content = {'changeEmailForm': ChangeEmailForm(),
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

    if request.method == 'GET':
        return render(request, 'profile.html', content)

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

    changeEmailForm = ChangeEmailForm(request.POST)
    if changeEmailForm.is_valid():
        newEmail = changeEmailForm.cleaned_data['newEmail']
        newEmailConfirm = changeEmailForm.cleaned_data['newEmailConfirm']
        if newEmail == newEmailConfirm:
            request.user.email = newEmail
            request.user.save()

    return redirect('/profile/')


@staff_member_required
def staff(request):
    organizations = Organization.objects.all()
    content = {'organizations': organizations}

    if request.method == 'GET':
        content.update({'organizationApplications': OrganizationApplication.objects.all(),
                        'organizationApplicationApproveConfirmationPopupData': {'prompt': None,
                                                                                'confirmButtonText': 'Approve',
                                                                                'formName': 'organizationApplicationIdToApprove',
                                                                                'formValue': None,
                                                                                'dismissButtonText': 'Cancel'},
                        'organizationApplicationDenyConfirmationPopupData': {'prompt': None,
                                                                             'confirmButtonText': 'Deny',
                                                                             'formName': 'organizationApplicationIdToDeny',
                                                                             'formValue': None,
                                                                             'dismissButtonText': 'Cancel'},
                        'organizationDeleteConfirmationPopupData': {'prompt': None,
                                                                   'confirmButtonText': 'Delete',
                                                                   'formName': 'organizationIdToDelete',
                                                                   'formValue': None, # Will be overriden in template
                                                                   'dismissButtonText': 'Cancel'}})
        return render(request, 'staff.html', content)

    organizationDeleteForm = OrganizationDeleteForm(request.POST)
    if organizationDeleteForm.is_valid():
        organizations.get(id=organizationDeleteForm.cleaned_data['organizationIdToDelete']).delete()
        return redirect('/staff/')

    organizationApplicationApproveForm = OrganizationApplicationApproveForm(request.POST)
    if organizationApplicationApproveForm.is_valid():
        organizationApplication = OrganizationApplication.objects.get(id=organizationApplicationApproveForm.cleaned_data['organizationApplicationIdToApprove'])

        # Create organization
        organization = Organization(name=organizationApplication.name, owner=organizationApplication.applicant)
        organization.save()

        # Assign organization to user
        organizationApplication.applicant.profile.organization = organization
        organizationApplication.applicant.profile.save()

        # Delete organization application
        organizationApplication.delete()

    organizationApplicationDenyForm = OrganizationApplicationDenyForm(request.POST)
    if organizationApplicationDenyForm.is_valid():
        organizationApplication = OrganizationApplication.objects.get(id=organizationApplicationDenyForm.cleaned_data['organizationApplicationIdToDeny'])

        # Delete organization application
        organizationApplication.delete()

    return redirect('/staff/')
