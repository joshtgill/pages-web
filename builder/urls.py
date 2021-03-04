from django.urls import path
from . import views


urlpatterns = [
    path('creator_upgrade/', views.creatorUpgrade, name='creator_upgrade'),
    path('create/', views.create, name='create'),
    path('create/builder/', views.builder, name='builder'),
    path('create/organization/', views.organization, name='organization')
]
