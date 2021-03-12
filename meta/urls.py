from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('create_account/', views.createAccount, name='create_account'),
    path('profile/', views.profile, name='profile'),
    path('staff/', views.staff, name='staff')
]
