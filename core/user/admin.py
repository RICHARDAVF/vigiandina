from django.contrib import admin
from .models import User,Empresa,Puesto,Unidad

from django.contrib.auth.models import Permission

class AdminUser(admin.ModelAdmin):
    list_display = ('username','last_name', 'first_name', 'dni', 'email')
admin.site.register(User, AdminUser)

class AdminEmpresa(admin.ModelAdmin):
    list_display = ('ruc',"razon_social")
admin.site.register(Empresa,AdminEmpresa)

class AdminUnidad(admin.ModelAdmin):
    list_display = ('unidad',"empresa")
admin.site.register(Unidad,AdminUnidad)

class AdminPuesto(admin.ModelAdmin):
    list_display = ('unidad',"puesto","direccion")
admin.site.register(Puesto,AdminPuesto)
class AdminPermission(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('content_type',)
    search_fields = ('name', 'content_type__app_label', 'codename')
admin.site.register(Permission, AdminPermission)

