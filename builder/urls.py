from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create, name='create'),
    path('create/select/', views.selectOrganization, name='select_organization'),
    path('create/apply/', views.applyOrganization, name='apply_organization'),
    path('create/builder/', views.builder, name='builder'),
    path('create/manage/', views.manageOrganization, name='manage_organization'),
    path('create/edit/', views.editOrganization, name='edit_organization')
]
