from django.urls import path
from .views.views import Dashboard, PageNotFoundView
from .report.views import ReporteControlAccesos
handler404 = PageNotFoundView.as_view()
app_name = 'dashboard'
urlpatterns = [
    # Otras URLs de tu aplicación
    path('report/', Dashboard.as_view(), name='dash_report'),
    path('pdf/reporte-1/', ReporteControlAccesos.as_view(), name='reporte_control_accesos'),
]
