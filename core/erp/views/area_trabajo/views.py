from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.erp.form.area_trabajo.forms import FormAreaTrabajo
from core.mixins import PermisosMixins
from ...models import AreaTrabajo

class CreateViewAreaTrabajo(LoginRequiredMixin,PermisosMixins,CreateView):
    login_url = reverse_lazy('login')
    permission_required = 'erp.add_area_trabajo'
    model = AreaTrabajo
    form_class = FormAreaTrabajo
    template_name = 'area_trabajo/create.html'
    success_url = reverse_lazy('erp:area_trabajo_list')
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
        context['title'] = 'creacion de una area de trabajo'
        context['entidad'] = 'Areas de trabajo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class ListViewAreaTrabajo(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = 'user.view_area_trabajo'
    model = AreaTrabajo
    template_name = 'area_trabajo/list.html'
    def get_queryset(self):
        return AreaTrabajo.objects.all()
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Listado de areas de trabajo"
        context['entidad'] = "Areas de trabajo"
        context['create_url'] = reverse_lazy('erp:area_trabajo_create')
        return context
class DeleteViewAreaTrabajo(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'user.delete_area_trabajo'
    model = AreaTrabajo
    success_url = reverse_lazy('erp:area_trabajo_list')
    url_redirect = success_url
    template_name = 'area_trabajo/delete.html'
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a esta area, primero elimine los registros que hagan referencia a esta area de trabajo'
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Eliminacion de una area de trabajo"
        context['entidad'] = 'Areas de trabajo'
        context['list_url'] = self.success_url
        return context
class UpdateViewAreaTrabajo(LoginRequiredMixin,PermisosMixins,UpdateView):
    login_url = reverse_lazy('login')
    permission_required = 'user.change_area_trabajo'
    model = AreaTrabajo
    form_class = FormAreaTrabajo
    template_name = 'area_trabajo/create.html'
    success_url = reverse_lazy('erp:area_trabajo_list')
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
        context['title'] = 'Edición de una Area de trabajo'
        context['entidad'] = 'Areas de trabajo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context