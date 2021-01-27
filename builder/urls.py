from django.urls import path
from . import views


urlpatterns = [
    path('creator_upgrade/', views.creatorUpgrade, name='creator_upgrade'),
    path('builder/', views.builder, name='builder'),
    path('page/', views.page, name='page')
]
