from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from core.erp.models import IngresoSalida, Visitas
from django.db.models import Count
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
            horas = Visitas.objects.filter(estado=3).annotate(hora=ExtractHour('h_inicio')).values('hora').annotate(total=Count('id')).order_by()
        else:
            horas = Visitas.objects.filter(Q(estado=3) &
                                       Q(user__empresa_id=self.request.user.empresa_id)).annotate(hora=ExtractHour('h_inicio')).values('hora').annotate(total=Count('id')).order_by()
        datos = {"hora":[],"cantidad":[] }
        for item in horas:
            datos['hora'].append(f"{item['hora']}H")
            datos['cantidad'].append(item['total'])
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
        # context["notify"] = json.dumps(list(Notification(self.request)))
        
        return context