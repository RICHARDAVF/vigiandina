
from django.shortcuts import render
from django.views.generic import View

class PageNotFoundView(View):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=404)
