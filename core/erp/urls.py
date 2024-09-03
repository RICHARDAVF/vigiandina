from django.urls import path
from .views.visitas.views import*
from .views.salas.views import*
from .views.parqueo.views import*
from .views.trabajadores.views import*
from .views.ingre_salidas.views import CreateViewIngSal,ListViewIngSal,UpdateViewIngSal,DeleteViewIngSal,AuditoriaIngSalView
from .views.empresas.views import*
from .views.unidad.views import*
from .views.puesto.views import*
from .views.equipos.views import*
from .views.cargos.views import*
from .views.views import PageNotFoundView
from .views.area_trabajo.views import CreateViewAreaTrabajo,ListViewAreaTrabajo,UpdateViewAreaTrabajo,DeleteViewAreaTrabajo
from .views.control_celepsa.views import CreateViewControlCelepsa
handler404 = PageNotFoundView.as_view()
app_name = 'erp'
urlpatterns = [
    #EMPRESAS
    path('empresa/list/',LisViewEmpresa.as_view(),name="empresa_list"),
    path('empresa/add/',CreateViewEmpresa.as_view(),name="empresa_create"),
    path('empresa/update/<int:pk>/',UpdateViewEmpresa.as_view(),name="empresa_update"),
    path('empresa/delete/<int:pk>/',DeleteViewEmpresa.as_view(),name="empresa_delete"),
    #UNIDAD
    path('unidad/list/',ListViewUnidad.as_view(),name='unidad_list'),
    path('unidad/add/',CreateViewUnidad.as_view(),name='unidad_create'),
    path('unidad/edit/<int:pk>/',UpdateViewUnidad.as_view(),name='unidad_update'),
    path('unidad/delete/<int:pk>/',DeleteViewUnidad.as_view(),name='unidad_delete'),
    #PUESTO
    path('puesto/list/',ListViewPuesto.as_view(),name='puesto_list'),
    path('puesto/add/',CreateViewPuesto.as_view(),name='puesto_create'),
    path('puesto/edit/<int:pk>/',UpdateViewPuesto.as_view(),name='puesto_update'),
    path('puesto/delete/<int:pk>/',DeleteViewPuesto.as_view(),name='puesto_delete'),
    #VISITAS
    path('visita/create/',CreateViewVisita.as_view(),name="visita_create"),
    path('visita/list/',ListViewVisita.as_view(),name="visita_list"),
    path('visita/update/<int:pk>/',UpdateViewVisita.as_view(),name="visita_edit"),
    path('visita/delete/<int:pk>/',DeleteViewVisita.as_view(),name="visita_delete"),
    path('visita/audi/<int:pk>/',AuditoriaVisitaView.as_view(),name="visita_audi"),
    #EQUIPOS DE PROTECCION DEL VISITANTE
    path('visita/ep/<int:pk>/',UpdateViewEquipos.as_view(),name="visita_ep_update"),

    #ASISTEN EN LA VISITA
    path('visita/asis/add/',CreateViewAsist.as_view(),name="asis_create"),
    #EPS
    path('epps/list/',ViewEPPS.as_view(),name="epps_list"),
    # path('visita/update/<int:pk>/',UpdateViewVisita.as_view(),name="visita_edit"),
    # path('visita/delete/<int:pk>/',DeleteViewVisita.as_view(),name="visita_delete"),
    #DELIVERY/COURRIER
    path('delivery/create/',CreateViewDelivery.as_view(),name="delivery_create"),
    path('delivery/update/<int:pk>/',UpdateViewDelivery.as_view(),name="delivery_edit"),
    #SALAS
    path('sala/create/',CreateViewSala.as_view(),name="sala_create"),
    path('sala/list/',ListViewSala.as_view(),name="sala_list"),
    path('sala/update/<int:pk>/',UpdateViewSala.as_view(),name="sala_edit"),
    path('sala/delete/<int:pk>/',DeleteViewSala.as_view(),name="sala_delete"),
    path('sala/audi/<int:pk>/',AuditoriaSalaView.as_view(),name="sala_audit"),
    #PARQUEO
    path('parqueo/create/',CreateViewParqueo.as_view(),name="parqueo_create"),
    path('parqueo/list/',ListViewParqueo.as_view(),name="parqueo_list"),
    path('parqueo/update/<int:pk>/',UpdateViewParqueo.as_view(),name="parqueo_edit"),
    path('parqueo/delete/<int:pk>/',DeleteViewParqueo.as_view(),name="parqueo_delete"),
    #CARGO TRABAJADOR
    path('cargo/create/',CreateViewCargo.as_view(),name="cargo_create"),
    path('cargo/list/',ListViewCargo.as_view(),name="cargo_list"),
    path('cargo/update/<int:pk>/',UpdateViewCargo.as_view(),name="cargo_edit"),
    path('cargo/delete/<int:pk>/',DeleteViewCargo.as_view(),name="cargo_delete"),
    #TRABAJADORES
    path('trab/create/',CreateViewTrabajador.as_view(),name="trabajador_create"),
    path('trab/list/',ListViewTrabajador.as_view(),name="trabajador_list"),
    path('trab/update/<int:pk>/',UpdateViewTrabajador.as_view(),name="trabajador_edit"),
    path('trab/delete/<int:pk>/',DeleteViewTrabajador.as_view(),name="trabajador_delete"),
    #INGRESO Y SALIDAS DE TRABAJADORES
    path('ingsal/list/',ListViewIngSal.as_view(),name='ingsal_list'),
    path('ingsal/add/',CreateViewIngSal.as_view(),name='ingsal_create'),
    path('ingsal/edit/<int:pk>/',UpdateViewIngSal.as_view(),name='ingsal_update'),
    path('ingsal/delete/<int:pk>/',DeleteViewIngSal.as_view(),name='ingsal_delete'),
    path('ingsal/audi/<int:pk>/',AuditoriaIngSalView.as_view(),name="ingsal_audi"),

    #UNIDADES DE TRABAJO
    path('area/trabajo/add/',CreateViewAreaTrabajo.as_view(),name='area_trabajo_create'),
    path('area/trabajo/list/',ListViewAreaTrabajo.as_view(),name='area_trabajo_list'),
    path('area/trabajo/update/<int:pk>/',UpdateViewAreaTrabajo.as_view(),name='area_trabajo_update'),
    path('area/trabajo/delete/<int:pk>/',DeleteViewAreaTrabajo.as_view(),name='area_trabajo_delete'),
    #CONTROL CELEPSA
    path("control/celepsa/add/",CreateViewControlCelepsa.as_view(),name="control_add"),
]