from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
import uuid
import django.contrib.auth as djangoAuth
from django.core.exceptions import ObjectDoesNotExist
from builder.models import CreatorUser


def home(request):
    return render(request, 'home.html')


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


def profile(request):
    content = {'changeEmailForm': ChangeEmailForm(),
               'customerDowngradeData': {'prompt': 'Downgrade <b>{}</b> from Creator to Customer?'.format(request.user.email),
                                         'confirmText': 'Downgrade',
                                         'action': 'DOWNGRADE'},
               'logoutConfirmationData': {'prompt': 'Logout of <b>{}</b>?'.format(request.user.email),
                                          'confirmText': 'Logout',
                                          'action': 'LOGOUT'},
               'createAccountConfirmationData': {'prompt': '''This will permanently delete the account associated
                                                              with <br><br><b>{}</b><br><br> All data will be lost
                                                              and this action cannot be undone.'''.format(request.user.email),
                                                 'confirmText': 'Delete account',
                                                 'action': 'DELETE_ACCOUNT'}}

    if request.method == 'GET':
        return render(request, 'profile.html', content)

    submittedConfirmationForm = ConfirmationForm(request.POST)
    submittedChangeEmailForm = ChangeEmailForm(request.POST)
    if submittedConfirmationForm.is_valid():
        if submittedConfirmationForm.cleaned_data['action'] == 'LOGOUT':
            djangoAuth.logout(request)
            return redirect('/login/')
        elif submittedConfirmationForm.cleaned_data['action'] == 'DELETE_ACCOUNT':
            deleteUsername = request.user.username
            djangoAuth.logout(request)
            User.objects.get(username=deleteUsername).delete()
            return redirect('/login/')
        elif submittedConfirmationForm.cleaned_data['action'] == 'DOWNGRADE':
            request.user.creatoruser.delete()
    elif submittedChangeEmailForm.is_valid():
        newEmail = submittedChangeEmailForm.cleaned_data['newEmail']
        newEmailConfirm = submittedChangeEmailForm.cleaned_data['newEmailConfirm']
        if newEmail == newEmailConfirm:
            request.user.email = newEmail
            request.user.save()

    return redirect('/profile/')
