from django.forms.models import BaseModelForm
from django.views.generic import CreateView,ListView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from core.mixins import PermisosMixins
from core.user.models import Unidad,Empresa
from core.erp.forms import FormUnidad
from django.urls import reverse_lazy
from django.http import JsonResponse

class CreateViewUnidad(LoginRequiredMixin,PermisosMixins,CreateView):
    permission_required = 'user.view_unidad'
    model = Unidad
    form_class = FormUnidad
    template_name = 'unidad/create.html'
    success_url = reverse_lazy('erp:unidad_list')
    
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action = request.POST['action']
            if action =='add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No se ingreso ninguna opcion"
        except Exception as e:
            data['error'] = f"Ocurrio un error: {str(e)}"
        return JsonResponse(data,safe=False)
    def get_form(self, form_class=None):
        form =  super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['empresa'].queryset = Empresa.objects.filter(id=self.request.user.empresa_id)
        else:
            form.fields['empresa'].queryset = Empresa.objects.all()
        return form
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['title'] = "Creacion de una unidad"
        context['entidad'] = 'Unidad'
        context['list_url'] = self.success_url
        context['action'] = "add"
        return context
class ListViewUnidad(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = 'user.view_unidad'
    model = Unidad
    template_name = 'unidad/list.html'
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Unidad.objects.select_related("empresa").filter(empresa_id=self.request.user.empresa_id)
        return Unidad.objects.select_related("empresa").all()
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Listado de Unidades"
        context['entidad'] = "Unidades"
        context['create_url'] = reverse_lazy('erp:unidad_create')
        return context
class DeleteViewUnidad(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'user.delete_unidad'
    model = Unidad
    success_url = reverse_lazy('erp:unidad_list')
    url_redirect = success_url
    template_name = 'unidad/delete.html'
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a esta unidad, primero elimine los registros que hagan referencia a esta unidad'
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Eliminacion de una unidad"
        context['entidad'] = 'Unidades'
        context['list_url'] = self.success_url
        return context
class UpdateViewUnidad(LoginRequiredMixin,PermisosMixins,UpdateView):
    login_url = reverse_lazy('login')
    permission_required = 'user.change_unidad'
    model = Unidad
    form_class = FormUnidad
    template_name = 'unidad/create.html'
    success_url = reverse_lazy('erp:unidad_list')
    url_redirect = success_url
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
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    def get_form(self, form_class=None):
        form =  super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['empresa'].queryset = Empresa.objects.filter(id=self.request.user.empresa_id)
        else:
            form.fields['empresa'].queryset = Empresa.objects.all()
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Unidad'
        context['entidad'] = 'Unidades'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context