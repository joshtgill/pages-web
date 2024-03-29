from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('meta.urls')),
    path('', include('builder.urls')),
    path('', include('client.urls'))
]
