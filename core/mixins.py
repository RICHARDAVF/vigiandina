from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
class PermisosMixins(object):
    permission_required = ''
    url_redirect = None
    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms
    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('dashboard:dash_report')
        return self.url_redirect
    def dispatch(self,request,*args,**kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request,*args,**kwargs)
        messages.error(request,'No tiene permiso para acceder a este modulo')
        return HttpResponseRedirect(self.get_url_redirect())

