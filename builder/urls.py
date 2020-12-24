from django.urls import path
from . import views


urlpatterns = [
    path('builder/', views.builder, name='builder'),
    path('page/', views.page, name='page')
]
