from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from django.http import HttpResponse
from core.custom_pdf import PDFControlAccesos
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_RIGHT,TA_CENTER,TA_LEFT
from django.utils import timezone
from reportlab.platypus import  Paragraph
from core.erp.models import Visitas,IngresoSalida
from django.db.models import Q
class ReporteControlAccesos(LoginRequiredMixin,View):
    login_url = reverse_lazy("login")
    def post(self,request,*args,**kwargs):
        date = {}
        
        action = request.POST["action"]
        if action == "report":
            desde = request.POST["desde"]
            hasta = request.POST["hasta"]
            data = Visitas.objects.filter(fecha__range=(desde,hasta))
            print(data)
            response = HttpResponse(content_type="application/pdf")
            filename = f"{self.request.user.username}-reporte-control-accesos.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            file = PDFControlAccesos(filename=filename,data=[],custom=self.custom_cabecera,request=self.request)
            file.generate()
            return response
            
    def custom_cabecera(canvas:Canvas,nombre):
        canvas.saveState()
        style = getSampleStyleSheet()
        repo = ParagraphStyle(name="aline",alignment=TA_CENTER,parent=style["Normal"])
        repo = Paragraph(f"<b>Reporte Control de ingresos</b>",style=repo)
        repo.wrap(nombre.width,nombre.topMargin)
        repo.drawOn(canvas,120,780)
        hora = ParagraphStyle(name="aline",alignment=TA_RIGHT,parent=style["Normal"])
        hora = Paragraph(f"<b>Fecha y Hora</b>: {timezone.now()}",style=hora)
        hora.wrap(nombre.width,nombre.topMargin)
        hora.drawOn(canvas,nombre.leftMargin,560)
        canvas.restoreState()