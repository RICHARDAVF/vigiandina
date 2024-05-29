from django.contrib import admin

from core.erp.models import CargoTrabajador,UnidadTrabajo

# Register your models here.
class AdminCargoView(admin.ModelAdmin):
    list_display = ('id','cargo')
admin.site.register(CargoTrabajador, AdminCargoView)



class AdminUnidadTrabajo(admin.ModelAdmin):
    list_display = ('id','unidad')
admin.site.register(UnidadTrabajo,AdminUnidadTrabajo)

