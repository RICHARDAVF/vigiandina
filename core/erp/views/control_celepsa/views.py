from django.views.generic import TemplateView
from django.http import JsonResponse
from core.erp.models import Trabajadores,ControlCelepsa
from django.utils import timezone
from datetime import datetime
import json
class CreateViewControlCelepsa(TemplateView):
    template_name = 'control/create.html'
    def post(self,request,*args,**kwargs):
      
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                codigo = request.POST['codigo_rfid'].strip()
                trabajador = Trabajadores.objects.get(codigo_rfid=codigo)
              
                try:
                    instance = ControlCelepsa.objects.get(trabajador=trabajador,hora_ingreso__isnull=False,hora_salida__isnull=True)
                    instance.hora_salida = timezone.now().strftime("%H:%M:%S")
                    instance.save()
                except:
                    instance = ControlCelepsa(trabajador=trabajador)
                    instance.save()
            else:
                data['error'] = "No se ingreso una opcion valida"
            data = self.get_data()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['title'] = "Control celepsa"
        context['entidad'] = 'Control'
        context['list_data'] = self.get_data()
        return context
    def get_data(self):
        data = []
        fecha = datetime.now().strftime("%Y-%m-%d")

        try:
            data = [
                {
                    "id": control.id,
                    "nombre": control.trabajador.nombre,
                    "hora_ingreso": self.format_date(control.hora_ingreso),
                    "hora_salida": self.format_date(control.hora_salida),
                    "fecha":control.fecha.strftime("%Y-%m-%d")
                }
                for control in ControlCelepsa.objects.filter(fecha=fecha)
            ] 
        except Exception as e:
            
            pass
  
        return json.dumps(data)
    def format_date(self,data:datetime):
        if data is None:
            return None
        return data.strftime("%H:%M:%S")
    