from django.forms.models import BaseModelForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisosMixins
from core.erp.models import IngresoSalida, Parqueo,Trabajadores
from core.erp.forms import FormIngSal
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
class CreateViewIngSal(LoginRequiredMixin,PermisosMixins,CreateView):
    permission_required = 'erp.add_ingresosalida'
    model = IngresoSalida
    form_class = FormIngSal
    template_name = 'ingre_salida/create.html'
    success_url = reverse_lazy('erp:ing_create')
    url_redirect = success_url
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action = request.POST['action']
            
            if action =='add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "no se envio ninguna opcion"
        except Exception as e:
            data['error'] = f"Ocurrio un error:{str(e)} "
        return JsonResponse(data)
    def get_form(self, form_class= None):
        form =  super().get_form(form_class)
        form.fields['usuario'].initial = self.request.user
        return form
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de un Ingreso'
        context['entidad'] = 'Ingresos'
        context['action'] = 'add'
        return context

class ListViewIngSal(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = 'erp.view_ingresosalida'
    login_url = reverse_lazy('login')
    model = IngresoSalida
    template_name = 'ingre_salida/list.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        fecha = timezone.now()
        try:
            action = request.POST['action']
            if action =="searchdata":
                data = []
                filter_superuser =  Q(fecha=fecha.strftime("%Y-%m-%d")) | Q(hora_salida__isnull=True)
                filter_user = Q(usuario__empresa_id=request.user.empresa_id) & (Q(fecha=fecha.strftime("%Y-%m-%d"))| Q(hora_salida__isnull=True))
                if request.user.is_superuser and (("desde" in request.POST and request.POST["desde"]!="") and ("hasta" in request.POST and request.POST["hasta"]!="")):
                    filter_superuser = Q(fecha__gte=request.POST["desde"]) & Q(fecha__lte=request.POST["hasta"])
                elif request.user.is_superuser==False and (("desde" in request.POST and request.POST["desde"]!="") and ("hasta" in request.POST and request.POST["hasta"]!="")):
                    filter_user = Q(usuario__empresa_id=request.user.empresa_id) & Q(fecha__gte=request.POST["desde"]) & Q(fecha__lte=request.POST["hasta"])
                if request.user.is_superuser:
                    instance = IngresoSalida.objects.filter(filter_superuser)
                else:
                    instance = IngresoSalida.objects.filter(filter_user)
                for value in instance:
                    item = value.toJSON()
                    item['documento'] = value.trabajador.documento
                    item['nombres'] = f"{value.trabajador.nombre}   {value.trabajador.apellidos}"
                    item['fecha'] = value.fecha.strftime('%Y-%m-%d')
                    item['hora_ingreso'] = value.hora_ingreso.strftime('%H:%M:%S')
                    data.append(item)
            elif action == 'confirm_hora_salida':
                instance = IngresoSalida.objects.get(Q(id=request.POST['id']) & Q(hora_salida__isnull=True))
                if instance.n_parqueo != None :
                    Parqueo.objects.filter(id=instance.n_parqueo_id).update(estado=True)
                instance.hora_salida = timezone.now().strftime('%H:%M:%S')
                instance.save()
            elif action == "search_trabajador":
                trabajadores = Trabajadores.objects.filter(
                    Q(estado=1) & (
                    Q(documento__icontains=request.POST['q']) | 
                    Q(nombre__icontains=request.POST['q']) | 
                    Q(apellidos__icontains=request.POST['q']) 
                    )
                    )
                data = []
                for index,value in enumerate(trabajadores):
                    item = {}
                    item['id'] = value.id
                    item['text'] = f"{value.nombre} {value.apellidos}"
                    data.append(item)
            elif action == "n_parkin":
                try:
                    
                    instance_parqueo = Parqueo.objects.get(numero=request.POST['parqueo'],unidad_id=request.user.unidad_id,puesto_id=request.user.puesto_id,estado=True)
                    instance = IngresoSalida.objects.get(id=request.POST['id'])
                    instance.n_parqueo = instance_parqueo
                    instance.save()
                    Parqueo.objects.filter(numero=request.POST['parqueo'],unidad_id=request.user.unidad_id,puesto_id=request.user.puesto_id).update(estado=False)
                except Parqueo.DoesNotExist  as e:
                    data['error'] = 'Parqueo no encontrado o esta ocupado'
            elif action == "search_for_date":
                pass
            else:
                data['error'] = 'No se envio ninguna opcion'
        except Exception as e:
            data['error'] = f"Ocurrio un error {str(e)}" 
        return JsonResponse(data,safe=False)
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de ingresos y salidas"
        context['list_url'] = reverse_lazy('erp:ingsal_list')
        context['entidad'] = 'Salidas'
        return context
class UpdateViewIngSal(LoginRequiredMixin,PermisosMixins,UpdateView):
    permission_required = 'erp.change_ingresosalida'
    login_url = reverse_lazy('login')
    model = IngresoSalida
    form_class = FormIngSal
    template_name = 'ingre_salida/create.html'
    success_url = reverse_lazy('erp:ingsal_list')
    url_redirect = success_url
    def dispatch(self,request,*args,**kwargs):
        self.object = self.get_object()
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = "No se ingreso ninguna opcion"
        except Exception as e:
            data['error'] = f"Ocurrio un erro: {str(e)}"
        return JsonResponse(data)
    def get_form(self, form_class= None):
        form =  super().get_form(form_class)
        form.fields['usuario'].initial = self.request.user
        form.fields['trabajador'].queryset = Trabajadores.objects.filter(estado=1)
        return form
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Edicion de un Ingreso O salida"
        context['entidad'] = "Ingresos y Salidas"
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context  
class DeleteViewIngSal(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'erp.delete_ingresosalida'
    login_url = reverse_lazy('login')
    model = IngresoSalida
    template_name = 'ingre_salida/delete.html'
    success_url = reverse_lazy('erp:ingsal_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Visita'
        context['Entidad'] = 'Visitas'
        context['list_url'] = self.success_url
        return context