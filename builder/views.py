from .models import *
from django.shortcuts import render


def builder(request):
    return render(request, 'builder.html', {'pages': Page.objects.all()})
