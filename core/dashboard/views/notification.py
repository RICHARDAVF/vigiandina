from django.utils import timezone
from core.erp.models import IngresoSalida
from django.db.models import Q
from datetime import timedelta
class Notification:
    def __init__(self,request):
        self.notify =[]
        self.request = request
        self.verify()
    def verify(self):
        try:
            fecha_actual = timezone.now()
            fecha_anterior = (fecha_actual-timedelta(days=1)).strftime("%Y-%m-%d")
            if self.request.user.is_superuser:
                
                trabajadores_sin_marcar = IngresoSalida.objects.filter(
                    Q(hora_ingreso__isnull=False) &
                    Q(hora_salida__isnull=True) &
                    Q(fecha__lt=fecha_anterior)
                        ).count()
                if trabajadores_sin_marcar>0:
                    noti_message = {
                        "message":f"Hay {trabajadores_sin_marcar} trabajadores que no marcaron hora de salida el dia de ayer",
                        
                    }
                    self.notify.append(noti_message)
            else:

                trabajadores_sin_marcar = IngresoSalida.objects.filter(
                    Q(hora_ingreso__isnull=False) &
                    Q(hora_salida__isnull=True) &
                    Q(usuario__empresa_id=self.request.user.empresa_id) &
                    Q(fecha__lt=fecha_anterior)
                        ).count()
             

                    
                if trabajadores_sin_marcar>0:
                    noti_message = {
                        "message":f"Hay {trabajadores_sin_marcar} trabajadores que no marcaron hora de salida el dia de ayer",
                        
                    }
                    self.notify.append(noti_message)

        except Exception as e:
            raise Exception (str(e))
    def __iter__(self):
        return iter(self.notify)