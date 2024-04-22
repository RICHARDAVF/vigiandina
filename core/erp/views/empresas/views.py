from typing import Any
from django.db import models
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from core.validation import Validation
from core.mixins import PermisosMixins
from core.user.models import Empresa
from core.erp.forms import FormEmpresa
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
class CreateViewEmpresa(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ('user.add_empresa',)
    model = Empresa
    form_class = FormEmpresa
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('erp:empresa_list')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "add":
                form = self.get_form()
                data = form.save()
            elif action =="search_ruc":
                data = Validation(request.POST['ruc'],'ruc').valid()
            else:
                data['error'] = f'No se ingreso ninguna opcion'
        except Exception as e:
            data['error'] = f"Ocurrio un error: {str(e)}"
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Creacion de una empresa"
        context['entidad'] = "Empresas"
        context['action'] = "add"
        context['list_url'] = self.success_url
        return context
class LisViewEmpresa(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required=('user.view_empresa',)
    model = Empresa
    template_name = 'empresa/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de Empresas"
        context['entidad'] = "Empresas"
        context['create_url'] = reverse_lazy('erp:empresa_create')
        return context
class UpdateViewEmpresa(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = 'user.change_empresa'
    login_url = reverse_lazy('login')
    model = Empresa
    form_class = FormEmpresa
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('erp:empresa_list')
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
            elif action =="search_ruc":
                data = Validation(request.POST['ruc'],'ruc').valid()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Empresa'
        context['entidad'] = 'Empresas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class DeleteViewEmpresa(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'user.delete_empresa'
    login_url = reverse_lazy('login')
    model = Empresa
    template_name = 'empresa/delete.html'
    success_url = reverse_lazy('erp:empresa_list')
    
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros con esta empresa, primero debe eliminar los registros que tenga como referencia a esta empresa'
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Empresa'
        context['Entidad'] = 'Empresas'
        context['list_url'] = self.success_url
        return context