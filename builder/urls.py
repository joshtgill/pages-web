from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.createPitch, name='create_pitch'),
    path('create/select/', views.selectOrganization, name='select_organization'),
    path('create/request/', views.requestNewOrganization, name='request_new_organization'),
    path('create/build/', views.build, name='build'),
    path('create/manage/', views.manageOrganization, name='manage_organization'),
    path('create/edit/', views.editOrganization, name='edit_organization')
]
