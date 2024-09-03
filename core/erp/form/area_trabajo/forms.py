from core.erp.models import AreaTrabajo
from django.forms import ModelForm,TextInput
class FormAreaTrabajo(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    class Meta:
        model = AreaTrabajo
        fields = '__all__'
        widgets = {
            'area':TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre de la area de trabajo'
                }
            )
        }
    def save(self,commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data