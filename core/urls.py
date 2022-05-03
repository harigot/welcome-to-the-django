from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hyper_api.urls', namespace='hyper_api')),
    path('', include('hyperdrated.urls', namespace='hyperdrated')),
]
