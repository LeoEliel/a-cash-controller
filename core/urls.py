from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuario.urls')),
    path('', include('financas.urls')),
    path('', include('dashboard.urls')),
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
]
