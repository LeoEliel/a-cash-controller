from django.urls import path

from .views import DashboardView, ExportarCSVView, ExportarPDFView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/exportar/csv/', ExportarCSVView.as_view(), name='exportar_csv'),
    path('dashboard/exportar/pdf/', ExportarPDFView.as_view(), name='exportar_pdf'),
]
