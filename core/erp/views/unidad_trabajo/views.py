from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.form.unidad_trabajo.forms import FormUnidadTrabajo
from core.mixins import PermisosMixins
from ...models import UnidadTrabajo

class CreateViewUnidadTrabajo(LoginRequiredMixin,PermisosMixins,CreateView):
    login_url = reverse_lazy('login')
    permission_required = 'erp.add_unidad_trabajo'
    model = UnidadTrabajo
    form_class = FormUnidadTrabajo
    template_name = 'unidad_trabajo/create.html'
    success_url = reverse_lazy('erp:unidad_trabajo_list')
    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action =='add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No se ingreso una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'creacion de una unidad de trabajo'
        context['entidad'] = 'Unidades de trabajo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class ListViewUnidadTrabajo(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = 'user.view_unidad_trabajo'
    model = UnidadTrabajo
    template_name = 'unidad_trabajo/list.html'
    def get_queryset(self):
        # CargarUnidadesTrabajo().cargar()
        # cargarUnidades1().cargar()
        return UnidadTrabajo.objects.all()
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Listado de Unidades de trabajo"
        context['entidad'] = "Unidades de trabajo"
        context['create_url'] = reverse_lazy('erp:unidad_trabajo_create')
        return context
class DeleteViewUnidadTrabajo(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'user.delete_unidad_trabajo'
    model = UnidadTrabajo
    success_url = reverse_lazy('erp:unidad_trabajo_list')
    url_redirect = success_url
    template_name = 'unidad_trabajo/delete.html'
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a esta unidad, primero elimine los registros que hagan referencia a esta unidad de trabajo'
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Eliminacion de una unidad de trabajo"
        context['entidad'] = 'Unidades de trabajo'
        context['list_url'] = self.success_url
        return context
class UpdateViewUnidadTrabajo(LoginRequiredMixin,PermisosMixins,UpdateView):
    login_url = reverse_lazy('login')
    permission_required = 'user.change_unidad_trabajo'
    model = UnidadTrabajo
    form_class = FormUnidadTrabajo
    template_name = 'unidad_trabajo/create.html'
    success_url = reverse_lazy('erp:unidad_trabajo_list')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Unidad de trabajo'
        context['entidad'] = 'Unidades de trabajo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context