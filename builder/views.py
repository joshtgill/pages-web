from .models import *
from django.shortcuts import render
from .forms import *


def builder(request):
    return render(request, 'builder.html', {'pageNames': [page.name for page in Page.objects.all()]})


def page(request):
    if request.method == 'GET':
        pageForm = PageForm(request.GET)
        if not pageForm.is_valid():
            render(request, 'page.html')

        page = Page.objects.get(name=pageForm.cleaned_data['name'])

        return render(request, 'page.html', {'page': page})

    return render(request, 'page.html')
