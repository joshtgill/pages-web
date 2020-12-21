from django.shortcuts import render
from .forms import CreateAccountForm, LoginForm, ProfileForm
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as djangoAuth


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

    return render(request, 'home.html')


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

    return render(request, 'home.html')


def profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')

    submittedProfileForm = ProfileForm(request.POST)
    if not submittedProfileForm.is_valid():
        return render(request, 'profile.html')

    if submittedProfileForm.cleaned_data['action'] == 'LOGOUT':
        djangoAuth.logout(request)
    else: # DELETE_ACCOUNT
        deleteUsername = request.user.username
        djangoAuth.logout(request)
        User.objects.get(username=deleteUsername).delete()

    return render(request, 'login.html', {'loginForm': LoginForm()})
