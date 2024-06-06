
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from core.mixins import PermisosMixins
from ...models import Parqueo,Unidad,Puesto
from ...forms import FormParqueo,FormParqueoAdmin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class CreateViewParqueo(LoginRequiredMixin,PermisosMixins,CreateView):
    permission_required = ('erp.add_parqueo',)
    login_url = reverse_lazy('login')
    model = Parqueo
    form_class = FormParqueoAdmin
    success_url = reverse_lazy('erp:parqueo_list')
    template_name = 'parqueo/create_parqueo_admin.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action =request.POST['action']
            if action == "add":
                if int(request.POST['desde'])<=int(request.POST['hasta']):
                    for num in range(int(request.POST['desde']),int(request.POST['hasta'])+1):
                        if Parqueo.objects.filter(
                                            numero=num,
                                            nombre=request.POST['nombre'],
                                            empresa_id=request.POST['empresa'],
                                            unidad_id=request.POST['unidad'],
                                            puesto_id=request.POST['puesto']
                                        ).exists():
                            data['error'] = "Ya existe parqueos en ese rango"
                            return JsonResponse(data)
                    for num in range(int(request.POST['desde']),int(request.POST['hasta'])+1):
                        Parqueo.objects.create(
                            numero=num,
                            nombre=request.POST['nombre'],
                            empresa_id=request.POST['empresa'],
                            unidad_id=request.POST['unidad'],
                            puesto_id=request.POST['puesto'])
                else:
                    data['error'] = 'ingreseo un rango incorrecto'
            elif action == 'search_unidad':
                data = []
                for value in Unidad.objects.filter(empresa_id=request.POST['id']):
                    data.append(value.toJSON())
            elif action == 'search_puesto':
                data = []
                for value in Puesto.objects.filter(unidad_id=request.POST['id']):
                    data.append(value.toJSON())
            else:
                data['error'] = 'No se a ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Creacion de parqueos'
        context['entidad'] = 'Parqueos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
       
        return context
class ListViewParqueo(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = ('erp.view_parqueo',)
    login_url = reverse_lazy('login')
    model = Parqueo
    template_name = 'parqueo/list.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
       
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                if not request.user.is_superuser:
                    for value in Parqueo.objects.filter(empresa_id=request.user.empresa_id):
                        item = value.toJSON()
                        data.append(item)
                else:
                    for value in Parqueo.objects.all():
                        item = value.toJSON()
                        data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
       
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Listado de Parqueos'
        context['create_url'] = reverse_lazy('erp:parqueo_create')
        context['list_url'] = reverse_lazy('erp:parqueo_list')
        context['entidad'] = 'Parqueos'
        return context
class UpdateViewParqueo(LoginRequiredMixin,PermisosMixins,UpdateView):
    permission_required = ('erp.change_parqueo',)

    login_url = reverse_lazy('login')
    model = Parqueo
    form_class = FormParqueo
    template_name = 'parqueo/create.html'
    success_url = reverse_lazy('erp:parqueo_list')
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
        context['title'] = 'Edición de un Parqueo'
        context['entidad'] = 'Parqueos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class DeleteViewParqueo(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = ('erp.delete_parqueo',)
    login_url = reverse_lazy('login')
    model = Parqueo
    template_name = 'parqueo/delete.html'
    success_url = reverse_lazy('erp:parqueo_list')
    
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a este parqueo, primero elimine los registros que hagan referencia a este parqueo'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Parqueo'
        context['Entidad'] = 'Parqueo'
        context['list_url'] = self.success_url
        return context