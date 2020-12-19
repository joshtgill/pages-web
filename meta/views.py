from django.shortcuts import render
from .forms import CreateAccountForm, LoginForm


def home(request):
    return render(request, 'home.html')


def createAccount(request):
    return render(request, 'create_account.html', {'createAccountForm': CreateAccountForm()})


def login(request):
    return render(request, 'login.html', {'loginForm': LoginForm()})
