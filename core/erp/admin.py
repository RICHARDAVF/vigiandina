from django.contrib import admin

from core.erp.models import CargoTrabajador,UnidadTrabajo,Trabajadores

# Register your models here.
class AdminCargoView(admin.ModelAdmin):
    list_display = ('id','cargo')
admin.site.register(CargoTrabajador, AdminCargoView)



class AdminUnidadTrabajo(admin.ModelAdmin):
    list_display = ('id','unidad')
admin.site.register(UnidadTrabajo,AdminUnidadTrabajo)

class AdminTrabajador(admin.ModelAdmin):
    list_display = ('tipo','documento','nombre','apellidos','telefono','direccion','empresa','cargo','estado')
    search_fields = ("nombre","empresa__razon_social")
admin.site.register(Trabajadores,AdminTrabajador)
