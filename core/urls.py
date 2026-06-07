from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuario.urls')),
    path('', include('financas.urls')),
    # Stub: redireciona '/' para transacoes até a M4 implementar o DashboardView
    path('', RedirectView.as_view(pattern_name='transacoes', permanent=False), name='dashboard'),
]
