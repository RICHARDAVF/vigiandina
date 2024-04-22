from django.urls import path

from core.user.views import *
app_name = 'user'
urlpatterns = [
    #USUARIO
    path('usuario/list/', ListViewUser.as_view(), name='user_list'),
    path('usuario/create/', CreateViewUser.as_view(), name='user_create'),
    path('usuario/delete/<int:pk>/', DeleteViewUser.as_view(), name='user_delete'),
    path('usuario/update/<int:pk>/', UpdateViewUser.as_view(), name='user_update'),
    path('usuario/change/group/<int:pk>/', UserChangeGroup.as_view(), name='user_change_group'),
    # path('usuario/perms/', SelectPermissionsView.as_view(), name='user_perms_create'),
    path('usuario/perms/<int:pk>/', UpdatePermissionsView.as_view(), name='user_perms_update'),

    
]