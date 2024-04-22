from django.urls import path
from .views.views import Dashboard, PageNotFoundView
handler404 = PageNotFoundView.as_view()
app_name = 'dashboard'
urlpatterns = [
    # Otras URLs de tu aplicación
    path('report/', Dashboard.as_view(), name='dash_report'),
]
