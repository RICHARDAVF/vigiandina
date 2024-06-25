import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from core.custom_pdf import PDFControlAccesos
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_RIGHT,TA_CENTER
from django.utils import timezone
from reportlab.platypus import  Paragraph
from core.erp.models import Visitas,IngresoSalida
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class ReporteControlAccesos(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self,request,*args,**kwargs):
        date = {}
        try:
            res = json.loads(request.body.decode("utf-8"))
   
            action = res.get("action")
            if action == "report":
                desde = res.get("desde")
                hasta = res.get("hasta")
            
                data = Visitas.objects.filter(fecha__range=(desde,hasta))
                values = [["Documento","Nombre","Apellidos","Fecha","Tipo"]]
                for value in data:
                    a = [value.dni,value.nombre,value.apellidos,value.fecha,"VISITA"]
                    values.append(a)
                data = IngresoSalida.objects.filter(fecha__range=(desde,hasta))
                for value in data:
                    a = [value.trabajador.documento,value.trabajador.nombre,value.trabajador.apellidos,value.fecha,"TRABAJADOR"]
                    values.append(a)
                response = HttpResponse(content_type="application/pdf")
                filename = f"{self.request.user.username}-reporte-control-accesos.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}" '
                file = PDFControlAccesos(filename=response,data=values,custom=self.custom_cabecera,request=self.request)
                file.generate()
           
                return response
            else:
                date["error"] = "Opcion invalida"
                
        except Exception as e:
        
            date["error"] = str(e)
        return JsonResponse(date,safe=False)
    def custom_cabecera(self,canvas:Canvas,nombre):
        canvas.saveState()
        style = getSampleStyleSheet()
        repo = ParagraphStyle(name="aline",alignment=TA_CENTER,parent=style["Normal"])
        repo = Paragraph(f"<b>REPORTE DE INGRESOS Y SALIDAS DE LA CORPORACION</b>",style=repo)
        repo.wrap(nombre.width,nombre.topMargin)
        repo.drawOn(canvas,0,750)
        hora = ParagraphStyle(name="aline",alignment=TA_RIGHT,parent=style["Normal"])
        hora = Paragraph(f"<b>Fecha y Hora</b>: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}",style=hora)
        hora.wrap(nombre.width,nombre.topMargin)
        hora.drawOn(canvas,nombre.leftMargin,780)
        canvas.restoreState()