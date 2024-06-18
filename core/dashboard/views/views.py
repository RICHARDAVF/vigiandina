from django.http import  JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from core.mixins import PermisosMixins
from core.erp.models import IngresoSalida, Visitas
from django.db.models import Count,F
from django.db.models.functions import ExtractHour,ExtractMonth
from datetime import datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
from .notification import Notification
from django.conf import settings
import os
from pandas import read_csv,to_datetime,DataFrame

# Create your views here.

class PageNotFoundView(View):
    template_name = 'dashboard/404.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)

class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'dashboard/dashboard.html'
    fecha_hora  = timezone.now()
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def prepare_fecha_hora(self,fecha_hora):
        return fecha_hora
    def post(self,request,*args,**kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'dash':
                
                data = []
                if self.request.user.is_superuser:
                    visitas_pro = Visitas.objects.select_related('sala').filter(estado=1)
                else:
                    visitas_pro = Visitas.objects.select_related('sala').filter(
                    Q(estado=1) & 
                    Q(user__empresa_id=self.request.user.empresa_id)
                    )
                for value in visitas_pro:
                    item = value.toJSON()
                    if value.sala_id is not None:
                        item['sala'] = value.sala.sala
                    fecha_registro = value.fecha
                    hora_registro = value.h_inicio
                    fecha_hora_registro = datetime.combine(fecha_registro, hora_registro)

                    if fecha_hora_registro >= datetime.strptime(request.POST['fecha_hora'], "%Y-%m-%dT%H:%M"):
                        data.append(value.toJSON())
    
           
            else:
                data['error'] = "Opcion incorrecta"
                    
        except Exception as e:
            data['error'] = f'Ocurrio un error {str(e)}'
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['entidad'] = 'Dashboard'
        if self.request.user.is_superuser:
            horas = Visitas.objects.filter(estado=3).annotate(hora=ExtractHour('h_inicio'),empresa_nombre=F('p_visita__empresa__razon_social')).values('hora','empresa_nombre').annotate(total=Count('id')).order_by()
        else:
            horas = Visitas.objects.filter(Q(estado=3) &
                                       Q(user__empresa_id=self.request.user.empresa_id)).annotate(hora=ExtractHour('h_inicio'),empresa_nombre=F('p_visita__empresa__razon_social')).values('hora','empresa_nombre').annotate(total=Count('id')).order_by()
        datos = {}
       
        hours = list(range(24))
        for values in horas:
            if values["empresa_nombre"] in datos:
                total = datos[values["empresa_nombre"]]["total"]
                total[values["hora"]+1]= values["total"]
                datos[values["empresa_nombre"]]["total"]= total
            else:
                total = [0]*24
                hor_ = hours
                total[values["hora"]+1] = values["total"]
                datos[values["empresa_nombre"]] = {"total":total,"hora":hor_}


        context['horas'] = json.dumps(datos)
        if self.request.user.is_superuser:
            mes = Visitas.objects.filter(estado=3).annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Count('id')).order_by()
        else:
            mes = Visitas.objects.filter(Q(estado=3) &
                                       Q(user__empresa_id=self.request.user.empresa_id)).annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Count('id')).order_by()

        m = {"1":'ENERO',"2":"FEBRERO","3":"MARZO","4":"ABRIL","5":"MAYO","6":"JUNIO","7":"JULIO","8":"AGOSTO","9":"SEPTIEMBRE","10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}
        datos = {'mes':[],'cantidad':[]}
        for item in mes:
            datos['mes'].append(m[str(item['mes'])])
            datos['cantidad'].append(item["total"])
        context['mes'] = json.dumps(datos)
        context['datetime_actual'] = timezone.now()
        if self.request.user.is_superuser:

            visitas:Visitas = Visitas.objects.filter(
                Q(h_llegada__isnull=False) &
                Q(h_salida__isnull=True) 
                )
        else:
            visitas:Visitas = Visitas.objects.filter(
                Q(h_llegada__isnull=False) &
                Q(h_salida__isnull=True) &
                Q(user__empresa_id=self.request.user.empresa_id)
                )
        total_personas = []
        context['cantidad_visitas'] = len(visitas)
        for value in visitas:
            
            item = {}
            item['nombres'] = f"{value.nombre} {value.apellidos}"
            item['documento'] = value.dni
            item['empresa'] = value.p_visita.empresa
            item['tipo'] = "VISITA"
            total_personas.append(item)
        if self.request.user.is_superuser:
            trabajadores:IngresoSalida = IngresoSalida.objects.filter(
                Q(hora_ingreso__isnull=False) &
                Q(hora_salida__isnull=True) 
                )
        else:
            trabajadores:IngresoSalida = IngresoSalida.objects.filter(
                Q(hora_ingreso__isnull=False) &
                Q(hora_salida__isnull=True) &
                Q(usuario__empresa_id=self.request.user.empresa_id)
                )
        for value in trabajadores:
       
            item = {}
            item['empresa'] = value.trabajador.empresa
            item['nombres'] = f"{value.trabajador.nombre} {value.trabajador.apellidos}"
            item['documento'] = value.trabajador.documento
            item['tipo'] = "TRABAJADOR"
            total_personas.append(item)
        
        context['lista_personas'] = total_personas
        context['total_personas'] = len(total_personas)
        context['cantidad_personal'] = len(trabajadores)
        context["notify"] = json.dumps(list(iter(Notification(self.request))))

        return context
class ShowAppMovil(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/list_data_app_movil.html"
    login_url = reverse_lazy("login")
    cantidad = 100
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def proccess_date(self,date:str):
        return date.split("/")[::-1]
    def post(self,request,*args,**kwagrs):
        data = {}
        try:
     
            if self.request.user.is_superuser or request.user.empresa_id==2:    
                filepath = os.path.join(settings.BASE_DIR,'static/files/asistencias_inma.csv')
                data_asistencia = read_csv(filepath_or_buffer=filepath,delimiter=";",header=None,names=["placa","nro_documento","nombres","empresa","fecha","hora_ingreso","tipo","id","hora_salida","motivo","numero_parkin","tipo_documento"],dtype=str)
                data_asistencia.fillna("",inplace=True)
                action = request.POST["action"]
                if action=="searchdata":
                    self.cantidad = int(request.POST['cantidad'])
                    if ("desde" in request.POST and request.POST["desde"]!='') and ("hasta" in request.POST and request.POST["hasta"]!=""):
                        data_init = to_datetime(request.POST["desde"])
                        data_finish = to_datetime(request.POST["hasta"])
                        data_asistencia["fecha"] = to_datetime(data_asistencia["fecha"])
                        data_filter:DataFrame = data_asistencia[(data_asistencia["fecha"]>=data_init) & (data_asistencia["fecha"]<=data_finish)]
                        data_filter["fecha"] = to_datetime(data_filter["fecha"]).dt.date
                        data = data_filter.to_dict(orient="records")

                    else:
                        data = data_asistencia[:self.cantidad].to_dict(orient="records") 
                    
                else:
                    data["error"] = "No se ingreso una opcion"
            else:
                data['error'] = " No tienes permisos para acceder a este modulo"
        except Exception as e:
            data["error"] = f"ocurrio un error: {str(e)}"
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Listado registros de la aplicacion movil, cantidad maxima 44748"
        return context
