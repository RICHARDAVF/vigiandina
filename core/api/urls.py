from django.urls import path
from .views import LoginView
app_name = 'api'
urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
]
