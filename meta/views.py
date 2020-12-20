from django.shortcuts import render
from .forms import CreateAccountForm, LoginForm
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def home(request):
    return render(request, 'home.html')


def createAccount(request):
    emptyCreateAccountForm = CreateAccountForm()

    if request.method == 'GET':
        return render(request, 'create_account.html', {'createAccountForm': emptyCreateAccountForm})

    submittedCreateAccountForm = CreateAccountForm(request.POST)
    if not submittedCreateAccountForm.is_valid():
        return render(request, 'create_account.html', {'createAccountForm': emptyCreateAccountForm})

    password = submittedCreateAccountForm.cleaned_data['password']
    if password == submittedCreateAccountForm.cleaned_data['repeatPassword']:
        createUser = User.objects.create_user(uuid.uuid4(), submittedCreateAccountForm.cleaned_data['email'], password)
        createUser.first_name = submittedCreateAccountForm.cleaned_data['firstName']
        createUser.last_name = submittedCreateAccountForm.cleaned_data['lastName']
        createUser.save()

    return render(request, 'home.html')


def login(request):
    emptyLoginForm = LoginForm()

    if request.method == 'GET':
        return render(request, 'login.html', {'loginForm': emptyLoginForm})

    submittedLoginForm = LoginForm(request.POST)
    if not submittedLoginForm.is_valid():
        return render(request, 'login.html', {'loginForm': emptyLoginForm})

    username = User.objects.get(email=submittedLoginForm.cleaned_data['email']).username
    loginUser = authenticate(username=username, password=submittedLoginForm.cleaned_data['password'])

    if loginUser:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html', {'loginForm': emptyLoginForm})
