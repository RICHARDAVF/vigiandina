from django.forms import ModelForm
from django import forms
from .models import User
from .models import Empresa,Unidad,Puesto
from django.contrib.auth.models import Permission
from django.db.models import Q

class PermissionSelectionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),to_field_name='id',widget=forms.Select(attrs={
        'class':'form-control',
    }),label="ID Usuario")
    tablas_excluir = ['historical','entry','group','permission','content','session','token']
    exclude_conditions = Q()
    for p_c  in tablas_excluir:
        exclude_conditions|=Q(name__icontains=p_c)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.exclude(exclude_conditions),
        widget=forms.CheckboxSelectMultiple,
    )
    
    class Meta:
        model = User
        fields = ['user', 'permissions']
    def __init__(self, *args, **kwargs):
        super(PermissionSelectionForm, self).__init__(*args, **kwargs)
        
        if self.instance:
            self.fields['user'].initial = self.instance.id
          
            self.fields['permissions'].initial = self.instance.user_permissions.all()
        self.fields['permissions'].label_from_instance = self.label_from_instance_custom

    def label_from_instance_custom(self, obj):
        return obj.name  # Utiliza el campo 'name' de Permission como etiqueta del checkb
class FormUser(ModelForm):
    empresa=forms.ModelChoiceField(queryset=Empresa.objects.all(),widget=forms.Select(attrs={
                "class":"form-control select2"
            }))
    unidad=forms.ModelChoiceField(queryset=Unidad.objects.all(),widget=forms.Select(attrs={
                "class":"form-control select2"
            }))
    puesto=forms.ModelChoiceField(queryset=Puesto.objects.all(),widget=forms.Select(attrs={
                "class":"form-control select2"
            }))
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','image','is_superuser','groups','dni',"empresa","unidad","puesto"]
        widgets = {
            'dni':forms.TextInput(
                attrs={
                    'placeholder':'Documento',
                    'class':'form-control',
                    'type':'number'
                }
            ),
            'first_name' : forms.TextInput(
                attrs={
                    'placeholder':'Ingrese sus nombres',
                    'class':'form-control',
                    'required':'true'
                }
            ),
            'last_name' : forms.TextInput(
                attrs={
                    'placeholder':'Ingrese sus apellidos',
                    'class':'form-control',
                    'required':'true'
                }
            ),
            'email' : forms.TextInput(
                attrs={
                    'placeholder':'Ingrese sus correo',
                    'type':'email',
                    'class':'form-control',
                }
            ),
            'username' : forms.TextInput(
                attrs={
                    'placeholder':'Ingrese su nombre de usuario',
                    'class':'form-control',
                }
            ),
            'password':forms.PasswordInput(render_value=True,attrs={
                'placeholder':'Ingrese su contraseña',
                'class':'form-control',
            }),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple',
                 
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'form-control', 
            }),
            'image':forms.FileInput(
                attrs={
                    'class':'form-control',
                    'type':'file'
            }),
        }
        exclude = ['user_permissions','last_login','date_joined','is_active','is_staff']
    def save(self,commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password!=pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['e'] = str(e)
        return data