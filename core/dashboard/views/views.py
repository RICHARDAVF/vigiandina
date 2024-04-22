from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from core.erp.models import Visitas
from django.db.models import Count
from django.db.models.functions import ExtractHour,ExtractMonth
from datetime import date,datetime
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import F, ExpressionWrapper, DateTimeField

# Create your views here.

class PageNotFoundView(View):
    template_name = 'dashboard/404.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)

class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'dashboard/dashboard.html'
    fecha_hora  = datetime.now()
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
               
                for value in Visitas.objects.select_related('sala').filter(estado=1):
                    item = value.toJSON()
                    if value.sala_id is not None:
                        item['sala'] = value.sala.sala
                    fecha_registro = value.fecha
                    hora_registro = value.h_inicio
                    fecha_hora_registro = datetime.combine(fecha_registro, hora_registro)

                    if fecha_hora_registro >= datetime.strptime(request.POST['fecha_hora'], "%Y-%m-%dT%H:%M"):
                        data.append(value.toJSON())
                   
        except Exception as e:
            print(str(e))
            # data['error'] = 'Ocurrio un error'
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['entidad'] = 'Dashboard'
        # context['visitas'] = Visitas.objects.filter(estado=1,).values('id','nombre','apellidos','sala',"fecha","h_inicio")
        horas = Visitas.objects.filter(estado=3).annotate(hora=ExtractHour('h_inicio')).values('hora').annotate(total=Count('id')).order_by()
        datos = {"hora":[],"cantidad":[] }
        for item in horas:
            datos['hora'].append(f"{item['hora']}H")
            datos['cantidad'].append(item['total'])
        context['horas'] = json.dumps(datos)
        mes = Visitas.objects.filter(estado=3).annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Count('id')).order_by()

        m={"1":'ENERO',"2":"FEBRERO","3":"MARZO","4":"ABRIL","5":"MAYO","6":"JUNIO","7":"JULIO","8":"AGOSTO","9":"SEPTIEMBRE","10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}
        datos = {'mes':[],'cantidad':[]}
        for item in mes:
            datos['mes'].append(m[str(item['mes'])])
            datos['cantidad'].append(item["total"])
        context['mes'] = json.dumps(datos)
        context['datetime_actual'] = datetime.now()
        return context