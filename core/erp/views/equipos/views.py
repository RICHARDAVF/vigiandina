
from typing import Any
from django.db import models
from django.http import JsonResponse
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.forms import FormEPVisitante
from core.erp.models import EquiposProteccionVisitante
class UpdateViewEquipos(LoginRequiredMixin,UpdateView):
    template_name = 'equipos/create.html'
    model = EquiposProteccionVisitante
    form_class = FormEPVisitante
    success_url = reverse_lazy('erp:visita_list')
    url_redirect = success_url
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
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
            data['error'] = f"Ocurrio un error: {str(e)}"
        return JsonResponse(data)
    def get_object(self, queryset=None):
        return self.model.objects.get(visitante_id=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = "Equipos de Porteccion"
        context['action'] = 'edit'
        context['list_url'] = self.success_url
        return context