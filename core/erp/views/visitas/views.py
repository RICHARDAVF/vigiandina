
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView,ListView,DeleteView,UpdateView,View
from core.mixins import PermisosMixins
from core.user.models import UserEmpresas,User
from core.validation import Validation
from ...forms import FormVisitas,FormDelivery
from ...models import Salas,Parqueo, Trabajadores,Visitas,Asistentes
from core.user.models import UserSupervisor
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date,time
from django.utils import timezone
from datetime import datetime
import json
# Create your views here.
class CreateViewVisita(LoginRequiredMixin,PermisosMixins,CreateView):
    login_url = reverse_lazy('login')
    permission_required = 'erp.add_visitas'
    model = Visitas
    form_class = FormVisitas
    template_name = 'visitas/create.html'
    success_url = reverse_lazy('erp:visita_list')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def valid_register(self):
        res = Visitas.objects.filter(dni=self.request.POST["dni"],h_salida__isnull=True,estado__in=['1','2','3'])
        return res.exists() 
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action =request.POST['action']
            if action == "add":
                if self.valid_register():
                    raise ValueError("No se marco hora de salida para esta visita")
                state,msg = self.validacion()
                if not state:
                    # data['error'] = msg
                    raise ValueError(msg)
                form = self.get_form()
                data = form.save()
        
                sala = request.POST['sala']
                if sala!='':
                    state_sale = Salas.objects.get(id=sala)
                    state_sale.estado = request.POST['estado']
                    state_sale.save()
                parqueo = request.POST['n_parqueo']
                if parqueo!='':
                    parking = Parqueo.objects.get(id=parqueo)
                    parking.estado = parqueo==''
                    parking.save()
            elif action=="search_doc_empresa":
                documento = request.POST["documento"]
                value = Visitas.objects.filter(documento_empresa=documento)
                
                if value.exists():
                    value = value.first()
           
                    data = {"empresa":value.empresa}
                else:
                    tipo = "dni" if len(documento)==8 else "ruc"
                    value = Validation(documento,tipo).valid()
             
                    if "error" in value:
                        data = value
                    else:
                        data = {"empresa":self.proccess_data(value["data"],tipo)}
           
            elif action =='searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
                
            else:
                data['error'] = 'No se a ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        form.fields['n_parqueo'].queryset=Parqueo.objects.filter(estado=True,empresa_id=self.request.user.empresa_id,
                                                        unidad_id=self.request.user.unidad_id,
                                                        puesto_id=self.request.user.puesto_id)
        form.fields['sala'].queryset=Salas.objects.filter(estado=0,empresa_id=self.request.user.empresa_id,
                                                        unidad_id=self.request.user.unidad_id,
                                                    puesto_id=self.request.user.puesto_id)
        values = UserEmpresas.objects.filter(usuario=self.request.user).values_list("empresa")
        if self.request.user.is_superuser:
            pass
        elif values.exists():
            form.fields["p_visita"].queryset = Trabajadores.objects.filter(empresa_id__in=values)
        else:
            form.fields['p_visita'].queryset = Trabajadores.objects.filter(empresa_id=self.request.user.empresa_id)
        initial_value = Trabajadores.objects.filter(nombre="PARA",apellidos="VISITAS DE SERVICIO").first()
        if initial_value:
            form.initial["p_visita"] = initial_value
        return form
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Creacion de Visitas'
        context['entidad'] = 'Visitas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
    def validacion(self):
        if self.request.method == 'POST':
            if self.request.POST['estado'] =='1' and self.request.POST['h_termino'].strip()=='':
                return False,'Hora de finalizacion incorrecta'
            return True,''
    def proccess_data(self,data,tipo):
        return data["nombre_completo"] if tipo=="dni" else data["nombre_o_razon_social"]

class ListViewVisita(LoginRequiredMixin,PermisosMixins,ListView):
    permission_required = 'erp.view_visitas'
    login_url = reverse_lazy('login')
    model = Visitas
    template_name = 'visitas/list.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def habilitar_sala(self,object):
        instace_sala = Salas.objects.get(id=object)
        instace_sala.estado = 0
        instace_sala.save()
    def validate_date(self):
        try:
            desde = self.request.POST["desde"]
            hasta = self.request.POST["hasta"]
            if desde!='' and hasta!='':
                return [desde,hasta,True]
            else: 
                raise
        except Exception as e:
            return [timezone.now().strftime("%Y-%m-%d"),timezone.now().strftime("%Y-%m-%d"),False]
    def validate_user(self):
        res = -1
        try:
            if int(self.request.POST['user'])!=-1:
                res = int(self.request.POST['user'])
        except:
            res = -1
        return res
    def post(self, request, *args, **kwargs):
        data = {}
        self.user = None
        
        try:
            action = request.POST['action']
            if action == 'searchdata':
                desde,hasta,state = self.validate_date()

                data = []
                try:
                    if request.user.is_superuser and state:
                        visitas = Visitas.objects.filter(fecha__gte=desde,fecha_salida__lte=hasta)
                    elif not request.user.is_superuser and state:
                        visitas = Visitas.objects.filter(user__empresa_id=self.request.user.empresa_id,fecha__gte=desde,fecha_salida__lte=hasta)
                    
                    else:
                        if request.user.is_superuser:
                            visitas = Visitas.objects.filter(Q(fecha=timezone.now().strftime("%Y-%m-%d")) | Q(h_salida__isnull=True),estado__in=["1","2","3"] )
                        else:
                            visitas = Visitas.objects.filter(
                                                            Q(fecha=timezone.now().strftime("%Y-%m-%d")) | Q(h_salida__isnull=True),
                                                            user__empresa_id=self.request.user.empresa_id,estado__in=["1","2","3"]
                                                    )
                    self.user = self.validate_user()
                    if self.user!=-1:
                        visitas = list(filter(lambda item:item.user.id==self.user,visitas))
                    for value in visitas:
                        item = value.toJSON() 
                        item['p_visita'] = f"{value.p_visita.nombre} {value.p_visita.apellidos}"
                        data.append(item)
                except Exception as e:
                    data = {}
                    data['error'] = str(e)
            elif action =="addperson":
                try:
                    data = {'asis':[],'parking':[]}
                    for index,value in  enumerate(Asistentes.objects.prefetch_related('n_parqueo').filter(visita_id=request.POST['id'])):
                        item = value.toJSON()
                        item['n_parqueo'] = value.n_parqueo.numero
                        data['asis'].append(item)
                    for value in Parqueo.objects.filter(estado=True,
                                                        empresa_id=request.user.empresa_id,
                                                        unidad_id=request.user.unidad_id,
                                                        puesto_id=request.user.puesto_id
                                                        ):
                        item = value.toJSON()
                        data['parking'].append(item)
                except Exception as e:
                    data['error'] = f"Ocurrio un erro {str(e)}"
            elif action =='confirm':
                instance = Visitas.objects.get(id=request.POST['id'])
                instance.h_llegada=timezone.now().strftime('%H:%M:%S')
                instance.estado=2
                instance.save()
            elif action =='h_final':
                instance = Visitas.objects.get(id=request.POST['id'])
                instance.h_salida = timezone.now().strftime('%H:%M:%S')
                instance.fecha_salida = timezone.now().strftime("%Y-%m-%d")
                sala = instance.sala_id
                if sala is not None:
                    self.habilitar_sala(sala)
                instance.estado = 3
                instance.save()
            elif action =="addvh":
                data = {}
                for value in Visitas.objects.filter(id=request.POST['id']).values_list("v_marca", "v_modelo", "v_placa", "fv_soat", "observacion","n_parqueo"):
                    try:
                        parqueo = Parqueo.objects.get(id=value[5]).numero
                    except:
                        parqueo = None
                    data['vh']={"v_marca":value[0],"v_modelo":value[1],"v_placa":value[2],"fv_soat":value[3],"n_parqueo":parqueo,'observacion':value[4]}
                   
                parqueos = []
                for value in Parqueo.objects.filter(estado=1,puesto_id=request.user.puesto_id).values_list("id","numero"):
                    parqueos.append({"id":value[0],"numero":value[1]})
                data['parking']=parqueos
            elif action=="h_salida":
                instance = Visitas.objects.get(id=request.POST['id'])
                instance.fecha_salida = timezone.now().strftime("%Y-%m-%d")
                hora = timezone.now().strftime("%H:%M:%S")
                instance.h_salida = hora
                if instance.h_termino is None:
                    instance.h_termino = hora
                sala = instance.sala_id
                if sala is not None:
                    self.habilitar_sala(sala)
                instance.estado = 3
                instance.save()
            elif action=="anular":
                instance = Visitas.objects.get(id=request.POST['id'])
                instance.estado = 0
                sala = instance.sala_id
                if sala is not None:
                   self.habilitar_sala(sala)
                instance.h_llegada = time(0,0)
                instance.h_salida = time(0,0)
                instance.save()
            elif action == "formvh":
                try:
                    instance_park = Parqueo.objects.get(id=int(request.POST['n_parqueo']))
                    instance = Visitas.objects.get(id=request.POST['id'])
                    instance.v_marca=request.POST['v_marca']
                    instance.v_modelo=request.POST['v_modelo']
                    instance.v_placa=request.POST['v_placa']
                    instance.fv_soat = request.POST['fv_soat']
                    instance.observacion = request.POST['observacion']
                    instance.n_parqueo = instance_park
                    instance.save()
                    instance_park.estado = 0
                    instance_park.save()
                except Exception as e:
                    
                    data['error'] = 'Seleccione un numero de parqueo'
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
       
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Listado de Visitas'
        context['create_url'] = reverse_lazy('erp:visita_create')
        context['list_url'] = reverse_lazy('erp:visita_list')
        context['entidad'] = 'Visitas'
        context["user_supervised"] = json.dumps(self.get_user_supervised())
        return context
    def get_user_supervised(self):
        if self.request.user.is_superuser:
            values = User.objects.all()
            data = [
                {
                    "id":value.id,
                    "value":value.username
                } for value in values
            ]  
        elif self.request.user.tipo_user=='2':
            values = UserSupervisor.objects.filter(supevisor_id=self.request.user.id)
            data = [
                {
                    "id":value.supervised_user.id,
                    "value":value.supervised_user.username
                } for value in values
            ] 
       
        else:
            data = []
        return data
class UpdateViewVisita(LoginRequiredMixin,PermisosMixins,UpdateView):
    permission_required = 'erp.change_visitas'
    login_url = reverse_lazy('login')
    model = Visitas
    form_class = FormVisitas
    template_name = 'visitas/create.html'
    success_url = reverse_lazy('erp:visita_list')
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
                
                sala = request.POST['sala']
                try:
                    instance = Salas.objects.get(id=sala)
                    instance.estado = 1
                    instance.save()

                except:
                    pass
                try:
                    int(request.POST['n_parqueo'])
                    instance = Parqueo.objects.get(id=request.POST['n_parqueo'])
                    instance.estado=True
                    instance.save()
                except :
                    pass
            elif action=="search_doc_empresa":
                documento = request.POST["documento"]
               
                value = Visitas.objects.filter(documento_empresa=documento)
                
                if value.exists():
                    value = value.first()
           
                    data = {"empresa":value.empresa}
                else:
                    tipo = "dni" if len(documento)==8 else "ruc"
                    value = Validation(documento,tipo).valid()
             
                    if "error" in value:
                        data = value
                    else:
                        data = {"empresa":self.proccess_data(value["data"],tipo)}
            elif action =='searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['sala'].queryset = Salas.objects.filter(estado=0)
        visitas_instance = self.object
        sala_actual = visitas_instance.sala
        salas_estado_0 = Salas.objects.filter(estado=0)
        try:
            salas_combinadas = list(salas_estado_0) + [sala_actual]
            salas_queryset = Salas.objects.filter(Q(pk__in=[sala.pk for sala in salas_combinadas]))
            form.fields['sala'].queryset = salas_queryset
            form.fields['n_parqueo'].queryset = Parqueo.objects.filter(estado=True)
        except Exception as e:
            pass
        try:
            parqueo_actual = visitas_instance.n_parqueo
            parqueos_estado_true = Parqueo.objects.filter(estado=True)
            parqueos_combinados = list(parqueos_estado_true) + [parqueo_actual]
            parqueos_queryset = Parqueo.objects.filter(Q(pk__in=[parqueo.pk for parqueo in parqueos_combinados]))
            form.fields['n_parqueo'].queryset = parqueos_queryset
        except Exception as e:
            pass
       
        if self.request.method == 'GET':
            form.fields['sala'].initial = sala_actual
            form.fields['n_parqueo'].initial = parqueo_actual
            # form.fields['p_visita'].initial = visitas_instance.p_visita.nombre
            
       
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Visita'
        context['entidad'] = 'Visitas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
    def proccess_data(self,data,tipo):
        return data["nombre_completo"] if tipo=="dni" else data["nombre_o_razon_social"]
class DeleteViewVisita(LoginRequiredMixin,PermisosMixins,DeleteView):
    permission_required = 'erp.delete_visitas'
    login_url = reverse_lazy('login')
    model = Visitas
    template_name = 'visitas/delete.html'
    success_url = reverse_lazy('erp:visita_list')
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if request.user.is_superuser:
                related_objects = self.object._meta.related_objects
                for related in related_objects:
                    related_name = related.get_accessor_name()
                    related_manager = getattr(self.object,related_name)
                    related_manager.all().delete()
                self.object.delete()
            else:
                data["error"] = "No tienes los permisos suficientes para realizar esta accion"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Visita'
        context['Entidad'] = 'Visitas'
        context['list_url'] = self.success_url
        return context
class CreateViewDelivery(LoginRequiredMixin,PermisosMixins,CreateView):
    permission_required = 'erp.add_visitas'
    login_url = reverse_lazy('login')
    model = Visitas
    form_class = FormDelivery
    template_name = "delivery/create.html"
    success_url = reverse_lazy('erp:visita_list')
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs) :
        data = {}
        try:
            action =request.POST['action']
            if action == "add":
                s,msg = self.validacion()
                if not s:
                    data['error'] = msg
                    return JsonResponse(data)
                form = self.get_form()
                data = form.save()
            elif action=="search_doc_empresa":
                documento = request.POST["documento"]
                try:
                    value = Visitas.objects.filter(documento_empresa=documento).first()
                    data = {"empresa":value.empresa}
                except Visitas.DoesNotExist:
                    tipo = "dni" if len(documento)==8 else "ruc"
                    value = Validation(documento,tipo).valid()
                   
                    if "error" in value:
                        data = value
                    else:
                        data = {"empresa":self.proccess_data(value["data"],tipo)}
           
            elif action =='searchdni':
                data = Validation(request.POST['dni'],'dni').valid()
               
            else:
                data['error'] = 'No se a ingresado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    def get_form(self,form_class=None):
        form = super().get_form(form_class)
        values = UserEmpresas.objects.filter(usuario=self.request.user).values_list("empresa")
        if self.request.user.is_superuser:
            pass
        elif values.exists():
            form.fields["p_visita"].queryset = Trabajadores.objects.filter(empresa_id__in=values)
        else:
            form.fields['p_visita'].queryset = Trabajadores.objects.filter(empresa_id=self.request.user.empresa_id)
        return form
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
       
        context['title'] = 'Creacion de Visitas'
        context['entidad'] = 'Visitas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
    def validacion(self):
       
        if self.request.POST['estado'] =='1' and self.request.POST['h_termino'].strip()=='':
            return False,'Hora de finalizacion incorrecta'
        return True,''
    def proccess_data(self,data,tipo):
        return data["nombre_completo"] if tipo=="dni" else data["nombre_o_razon_social"]

class UpdateViewDelivery(LoginRequiredMixin,PermisosMixins,UpdateView):
    permission_required = 'erp.change_visitas'

    login_url = reverse_lazy('login')
    model = Visitas
    form_class = FormDelivery
    template_name = 'delivery/create.html'
    success_url = reverse_lazy('erp:visita_list')
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
        context['title'] = 'Edición de una Visita'
        context['entidad'] = 'Delivery'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context  
class CreateViewAsist(LoginRequiredMixin,PermisosMixins,View):
    permission_required = 'erp.add_visitas'

    login_url = reverse_lazy('login')
    model = Asistentes
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)
    def post(self,request,*ars,**kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == "addperson":
                id = request.POST['id']
                if request.POST['soat_v']=='':
                    fecha = date(1, 1, 1)
                else:
                    fecha = request.POST['soat_v']
                try:
                    sctr = request.FILES.get('sctr', None)
                    park = Parqueo.objects.get(id=request.POST['n_parqueo'])
                    park.estado = 0
                    asis = Asistentes.objects.create(
                            visita_id=int(id),
                            documento=request.POST['documento'],
                            nombre=request.POST['nombre'],
                            apellidos = request.POST['apellidos'],
                            empresa = request.POST['empresa'],
                            marca_v=request.POST['marca_v'],
                            modelo_v=request.POST['modelo_v'],
                            placa_v=request.POST['placa_v'],
                            soat_v=fecha,
                            sctr=sctr,
                            n_parqueo=park,
                        )
                    asis.save()
                    park.save()
                   
                
                except Exception as e:
                
                    data['error'] = f"Ocurrio un error: {str(e)}"
            elif action =='lib_park':
                id_park = Asistentes.objects.get(id=request.POST['id'])
                instance = Parqueo.objects.get(id=id_park.n_parqueo_id)
                instance.estado = True
                instance.save()
            data = []
            for value in Asistentes.objects.filter(visita_id=int(id)):
                item = value.toJSON()
                item['n_parqueo'] = value.n_parqueo.numero
                data.append(item)
        except Exception as e:
            data['error'] = 'Ocurrio un error'

        return JsonResponse(data,safe=False)
class AuditoriaVisitaView(LoginRequiredMixin,PermisosMixins,ListView):
    login_url = reverse_lazy('login')
    permission_required = 'erp.view_visitas'
    model  = Visitas
    template_name = 'visitas/auditoria.html'
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_superuser:
            # Redirige a la página desde la que vino, o a una página de acceso denegado.
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return super().dispatch(request,*args,**kwargs)
    def get_queryset(self):
        instance = Visitas.objects.get(id=self.kwargs['pk'])
        return instance.history.all()
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Auditoria de una visita"
        return context