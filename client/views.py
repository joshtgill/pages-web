from django.shortcuts import render, redirect
from .forms import *
from builder.models import Organization
from django.core.exceptions import ObjectDoesNotExist


def explore(request):
    if request.method == 'GET':
        organizationSearchForm = OrganizationSearchForm(request.GET)

        # If no search text is provided, go to explore page
        if not organizationSearchForm.is_valid():
            return render(request, 'explore.html', {'organizationSearchForm': OrganizationSearchForm()})

        # If the searched organization name does not exist, return to explore page
        try:
            organization = Organization.objects.get(name__iexact=organizationSearchForm.cleaned_data['organizationName'])
        except ObjectDoesNotExist:
            return redirect('/explore/')

        return render(request, 'home.html')
