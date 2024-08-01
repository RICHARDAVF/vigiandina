from django.views.generic import TemplateView
from django.http import JsonResponse
class CreateViewControlCelepsa(TemplateView):
    template_name = 'control/create.html'
    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                pass
            else:
                data['error'] = "No se ingreso una opcion valida"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['title'] = "Control celepsa"
        context['entidad'] = 'Control'
        # context['list_url'] = self.success_url
        return context