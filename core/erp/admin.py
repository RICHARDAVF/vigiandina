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
class AdminVisitas(admin.ModelAdmin):
    list_display = ('id','user__username','dni','nombre','apellidos','empresa')
    search_fields = ('user__username','dni','nombre','id')
admin.site.register(Visitas,AdminVisitas)
class AdminIngresoSalida(admin.ModelAdmin):
    list_display = ('id','usuario__username','trabajador','fecha_ingreso','hora_ingreso','fecha_salida','hora_salida')
    search_fields = ('id','usuario__username','trabajador')
admin.site.register(IngresoSalida,AdminIngresoSalida)
