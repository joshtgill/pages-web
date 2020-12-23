from django.urls import path
from . import views


urlpatterns = [
    path('builder/', views.builder, name='builder')
]
