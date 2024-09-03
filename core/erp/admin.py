from django.contrib import admin

from core.erp.models import CargoTrabajador,AreaTrabajo,Trabajadores,Visitas,IngresoSalida

# Register your models here.
class AdminCargoView(admin.ModelAdmin):
    list_display = ('id','cargo')
admin.site.register(CargoTrabajador, AdminCargoView)



class AdminAreaTrabajo(admin.ModelAdmin):
    list_display = ('id','area')
admin.site.register(AreaTrabajo,AdminAreaTrabajo)

class AdminTrabajador(admin.ModelAdmin):
    list_display = ('tipo','documento','nombre','apellidos','telefono','direccion','empresa','cargo','estado')
    search_fields = ("nombre","empresa__razon_social")
admin.site.register(Trabajadores,AdminTrabajador)
admin.site.register(Visitas)
admin.site.register(IngresoSalida)
