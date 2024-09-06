from django.contrib import admin
from .models import User,Empresa,Puesto,Unidad,UserEmpresas,UserSupervisor

from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from .forms import FormUser,UserCreationForm
class UserAdminModel(UserAdmin):
    fomr = FormUser
    add_form = UserCreationForm
admin.site.register(User,UserAdminModel)
# class AdminUser(admin.ModelAdmin):
#     list_display = ('username','last_name', 'first_name', 'dni', 'email')
# admin.site.register(User, AdminUser)

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
class AdminUserEmpresa(admin.ModelAdmin):
    list_display = ('usuario__username','empresa')
    search_fields = ('usuario_username','empresa')
admin.site.register(UserEmpresas,AdminUserEmpresa)
class AdminUserSupervisor(admin.ModelAdmin):
    list_display = ("supervisor","supervised_user")
admin.site.register(UserSupervisor,AdminUserSupervisor)
