
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView,ListView,DeleteView,UpdateView,TemplateView
from core.mixins import PermisosMixins
from ...models import Salas
from ...forms import FormSala
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CreateViewSala(LoginRequiredMixin,PermisosMixins,CreateView):
    login_url = reverse_lazy('login')
    permission_required = "erp.add_salas"
    model = Salas
    form_class = FormSala
    template_name = 'salas/create.html'
    success_url = reverse_lazy('erp:sala_list')
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

        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una Sala'
        context['entidad'] = 'Salas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
class ListViewSala(LoginRequiredMixin,PermisosMixins,ListView):
    login_url = reverse_lazy('login')
    permission_required = "erp.view_salas"
    model = Salas
    template_name = 'salas/list.html'
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
                    for value in Salas.objects.filter(empresa_id=request.user.empresa_id,unidad_id=request.user.unidad_id,puesto_id=request.user.puesto_id):
                        item = value.toJSON()
                        data.append(item)
                else:
                    for value in Salas.objects.all():
                        item = value.toJSON()
                        data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
       
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Listado de Salas'
        context['create_url'] = reverse_lazy('erp:sala_create')
        context['list_url'] = reverse_lazy('erp:sala_list')
        context['entidad'] = 'Salas'
        return context
class UpdateViewSala(LoginRequiredMixin,PermisosMixins,UpdateView):
    login_url = reverse_lazy('login')
    permission_required = "erp.change_salas"
    model = Salas
    form_class = FormSala
    template_name = 'salas/create.html'
    success_url = reverse_lazy('erp:sala_list')
   
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
        context['title'] = 'Edición de un Sala'
        context['entidad'] = 'Salas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class DeleteViewSala(LoginRequiredMixin,PermisosMixins,DeleteView):
    login_url = reverse_lazy('login')
    permission_required = "erp.delete_salas"
    model = Salas
    template_name = 'salas/delete.html'
    success_url = reverse_lazy('erp:sala_list')
    
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Existe registros que hacen referencia a esta sala, primero elimine los regsitros que tengan como referencia esta sala'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Sala'
        context['Entidad'] = 'Salas'
        context['list_url'] = self.success_url
        return context
class AuditoriaSalaView(LoginRequiredMixin,PermisosMixins,ListView):
    login_url = reverse_lazy('login')
    permission_required = 'erp.view_salas'
    model  = Salas
    template_name = 'salas/auditoria.html'
  
    def get_queryset(self):
        instace =  Salas.objects.get(id=self.kwargs['pk'])
        return instace.history.all()
    def get_context_data(self, **kwargs):
        context =   super().get_context_data(**kwargs)
        context['title'] = "Auditoria de una sala"
        sala = Salas.objects.get(id=self.kwargs['pk'])
        context['sala'] = {'empresa':sala.empresa,'unidad':sala.unidad,'puesto':sala.puesto}
        return context

        