from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from crum import get_current_request
from simple_history.models import HistoricalRecords
from config.settings import MEDIA_URL, STATIC_URL
class Empresa(models.Model):
    ruc = models.CharField(max_length=11,verbose_name="RUC",unique=True)
    razon_social = models.CharField(max_length=150,verbose_name="Razon social")
    direccion = models.CharField(max_length=150,verbose_name="Direccion",null=True,blank=True)
    # history = HistoricalRecords()
    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = "empresas"
        db_table = 'empresas'
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self) -> str:
        return str(self.razon_social)
class Unidad(models.Model):
    empresa = models.ForeignKey(Empresa,on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name="Empresa")
    unidad = models.CharField(max_length=150,verbose_name="Unidad")
    # history = HistoricalRecords()

    class Meta:
        verbose_name = "unidad"
        verbose_name_plural = "unidades"
        db_table = 'unidades'
    def toJSON(self):
        item = model_to_dict(self)
        # item['empresa'] = self.empresa.id
        return item 
    def __str__(self) -> str:
        return str(self.unidad)
class Puesto(models.Model):
    unidad = models.ForeignKey(Unidad,on_delete=models.DO_NOTHING,verbose_name="Unidad")
    puesto = models.CharField(max_length=15,verbose_name="Puesto")
    direccion = models.CharField(max_length=150,verbose_name="Direccion")
    # history = HistoricalRecords()
    class Meta:
        verbose_name = "puesto"
        verbose_name_plural = "puestos"
        db_table = 'puestos'
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self) -> str:
        return str(self.puesto)
class User(AbstractUser):
    dni = models.CharField(max_length=10,verbose_name="Documento",null=True,blank=True)
    tipo = models.CharField(max_length=255,null=True,blank=True,verbose_name="Tipo de Usuario")
    image = models.ImageField(upload_to='users/',null=True,blank=True,verbose_name="Imagen")
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True,verbose_name="Token")
    last_name = models.CharField(max_length=150, blank=False,verbose_name='Nombre')
    first_name = models.CharField(max_length=30, blank=False,verbose_name="Apellidos")
    empresa = models.ForeignKey(Empresa,on_delete=models.DO_NOTHING,verbose_name="Empresa",null=True,blank=True)
    unidad = models.ForeignKey(Unidad,on_delete=models.DO_NOTHING,verbose_name='Unidad',null=True,blank=True)
    puesto = models.ForeignKey(Puesto,on_delete=models.DO_NOTHING,verbose_name='Puesto',null=True,blank=True)
    # history = HistoricalRecords()

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]   
        return item
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
    def __str__(self):
        return str(self.id)
class TokenBearer(models.Model):
    token = models.CharField(max_length=250,verbose_name="Token")
    nombre = models.CharField(max_length=50,verbose_name="Nombre del proveedor")
    descripcion = models.CharField(max_length=150,verbose_name="Descripcion")
    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'
        db_table = 'tokens'
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
class UserEmpresas(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name="Usuario")
    empresa = models.ForeignKey(Empresa,on_delete=models.DO_NOTHING,verbose_name="Empresas")
    class Meta:
        verbose_name = "Empresa asignada"
        verbose_name_plural = "Empresas asignadas"
        db_table = "user_empresas"
    def toJSON(self):
        item = model_to_dict(self)
        return item
    def __str__(self) -> str:
        return f"{self.usuario.username}"