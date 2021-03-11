from django.urls import path
from . import views


urlpatterns = [
    path('creator_upgrade/', views.creatorUpgrade, name='creator_upgrade'),
    path('create/', views.create, name='create'),
    path('create/builder/', views.builder, name='builder'),
    path('create/manage/', views.manageOrganization, name='manage_organization'),
    path('create/edit/', views.editOrganization, name='edit_organization')
]
