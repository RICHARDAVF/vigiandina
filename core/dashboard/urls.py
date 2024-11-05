from django.urls import path
from .views.views import Dashboard1, PageNotFoundView,ShowAppMovil,Dashboard
from .report.views import ReporteControlAccesos
handler404 = PageNotFoundView.as_view()
app_name = 'dashboard'
urlpatterns = [
    # Otras URLs de tu aplicación
    path('report/', Dashboard.as_view(), name='dash_report'),
    # path('report/', Dashboard1.as_view(), name='dash_report'),
    path('pdf/reporte-1/', ReporteControlAccesos.as_view(), name='reporte_control_accesos'),
    path('data/movil/', ShowAppMovil.as_view(), name='list_data_movil'),
]
