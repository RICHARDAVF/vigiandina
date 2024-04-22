
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView,ListView,DeleteView,UpdateView,TemplateView
from core.mixins import PermisosMixins
from ...models import CargoTrabajador
from ...forms import FormCargo
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreateViewCargo(LoginRequiredMixin,PermisosMixins,CreateView):
    login_url = reverse_lazy('login')
    permission_required = "erp.add_cargos"
    model = CargoTrabajador
    form_class = FormCargo
    template_name = 'cargos/create.html'
    success_url = reverse_lazy('erp:cargo_list')
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action =request.POST['action']
            if action == "add":
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No se a ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Creacion de un Cargo'
        context['entidad'] = 'Cargos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class ListViewCargo(LoginRequiredMixin,PermisosMixins,ListView):
    login_url = reverse_lazy('login')
    permission_required = "erp.view_cargos"
    model = CargoTrabajador
    template_name = 'cargos/list.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
       
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for value in CargoTrabajador.objects.all():
                    item = value.toJSON()
                    # item['unidad'] = value.unidad.unidad if value.unidad!= None else ''
                    data.append(item)
             
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
       
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cargos'
        context['create_url'] = reverse_lazy('erp:cargo_create')
        context['list_url'] = reverse_lazy('erp:cargo_list')
        context['entidad'] = 'Cargos'
        return context
class UpdateViewCargo(LoginRequiredMixin,PermisosMixins,UpdateView):
    login_url = reverse_lazy('login')
    permission_required = "erp.change_cargos"
    model = CargoTrabajador
    form_class = FormCargo
    template_name = 'cargos/create.html'
    success_url = reverse_lazy('erp:cargo_list')
   
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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Cargo'
        context['entidad'] = 'Cargos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class DeleteViewCargo(LoginRequiredMixin,PermisosMixins,DeleteView):
    login_url = reverse_lazy('login')
    permission_required = "erp.delete_cargos"
    model = CargoTrabajador
    template_name = 'cargos/delete.html'
    success_url = reverse_lazy('erp:cargo_list')
    
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a este cargo, primero elimine esos registro'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Cargo'
        context['entidad'] = 'Cargos'
        context['list_url'] = self.success_url
        return context
