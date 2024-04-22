from typing import Any
from django import http
from django.http import JsonResponse
from django.views.generic import View
from core.validation import Validation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
class SearchDoc(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    def post(self,request,*args,**kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_doc':
                data = Validation(request.POST['doc'],'dni').valid()
        except Exception as e:
            data['error'] = f" Ocurrio un error: {str(e)}"
        return JsonResponse(data,safe=False)
