from typing import Any
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from core.mixins import PermisosMixins
from core.validation import Validation
from core.user.forms import FormUser
from core.user.models import User,Puesto,Unidad
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PermissionSelectionForm

class ListViewUser(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = ('user.view_user',)
    login_url = reverse_lazy('login')
    model = User
    template_name = 'user/list.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
           
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entidad'] = 'Usuarios'
        context['is_superuser'] = self.request.user.is_superuser
        return context
class CreateViewUser(LoginRequiredMixin,PermisosMixins,CreateView):
    permission_required = ('user.view_user','user.create_user')
    login_url = reverse_lazy('login')
    model = User
    form_class = User
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    url_redirect = success_url
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}        
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            elif action =='searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
            elif action == 'search_unidad':
                data = []
                for value in Unidad.objects.filter(empresa_id=request.POST['id']):
                    data.append(value.toJSON())
            elif action == 'search_puesto':
                data = []
                for value in Puesto.objects.filter(unidad_id=request.POST['id']):
                    data.append(value.toJSON())
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entidad'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class UpdateViewUser(LoginRequiredMixin,PermisosMixins,UpdateView):
    permission_required = ('user.view_user','user.update_user')
    login_url = reverse_lazy('login')
    model = User
    form_class = FormUser
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    url_redirect = success_url
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
  
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            elif action =='searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
            elif action == 'search_unidad':
                data = []
                for value in Unidad.objects.filter(empresa_id=request.POST['id']):
                    data.append(value.toJSON())
            elif action == 'search_puesto':
                data = []
                for value in Puesto.objects.filter(unidad_id=request.POST['id']):
                    data.append(value.toJSON())
            elif action == 'searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entidad'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class DeleteViewUser(LoginRequiredMixin,DeleteView):
    permission_required = ('user.view_user','user.delete_user')
    login_url = reverse_lazy('login')
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:user_list')
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'El usuario tiene registros relacionados, primero elimine los registros que hagan referencia al usuario'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Usuario'
        context['entidad'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context
class UserChangeGroup(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('user:user_list'))


class SelectPermissionsView(CreateView):
    form_class = PermissionSelectionForm
    template_name = 'user/perms.html'  
    success_url = reverse_lazy('user:user_list')  

    def form_valid(self, form):
        data = {}
        try:
            user = form.cleaned_data['user']
            selected_permissions = form.cleaned_data['permissions']
            user.user_permissions.set(selected_permissions)
        except Exception as e:
            data['error'] = f"Ocurrio un error {str(e)}"
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Asignacion de Permisos"
        context['list_url'] = self.success_url
        context['entidad'] = "Permisos"
        return context

class UpdatePermissionsView(UpdateView):
    model = User
    form_class = PermissionSelectionForm
    template_name = 'user/perms.html'
    success_url = reverse_lazy('user:user_list')

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(pk=user_id)
        self.object = user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Permisos"
        context['entidad'] = "Permisos"
        context['list_url'] = self.success_url
        context['username'] = User.objects.get(id=self.object.id)
        context['action'] = 'edit'
        return context
    def post(self, request, *args, **kwargs):
        data = {}
        if int(request.POST['user'])!=int(kwargs['pk']):
            return JsonResponse({'error':'No se puede cambiar de usuario'})
        
        try:
            action = request.POST['action']
            if action =='edit':
                user = User.objects.get(id=request.POST['user'])
                try:
                    selected_permissions = request.POST.getlist('permissions')
                    user.user_permissions.set(selected_permissions)
                except :
                    user.user_permissions.clear()
      
            else:
                data['error']  = "No ingreso ninguna opcion"
        except:
            data['error'] = f'Error al registrar'
        return JsonResponse(data)