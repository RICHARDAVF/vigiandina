from pandas import read_excel
from core.erp.models import CargoTrabajador,Trabajadores, UnidadTrabajo

class Cargo:
    def __init__(self):
        self.df  = read_excel(r"C:\inetpub\wwwroot\app\test\Personal de empresas del Edificio INMA.xlsx",dtype=str)
    def cargar(self):
        
        for item in self.df['CARGO'].to_list():
           
            try:
                car = CargoTrabajador(cargo=item)
                car.save()
            except Exception as e:
               pass
    def trabajadores(self):
        dni = self.df['DNI'].to_list()
        cargo = self.df['CARGO'].to_list()
        nombre = self.df['NOMBRE'].to_list()
        apellidos = self.df['APELLIDOS'].to_list()
        empresa = self.df['EMPRESA'].to_list()
        for doc,car,name,last,em in zip(dni,cargo,nombre,apellidos,empresa):
            tipo = "1"
            carg = CargoTrabajador.objects.get(cargo=car)
            if len(doc)!=8:
                tipo = '2'
            try:
                Trabajadores.objects.create(
                    cargo=carg,
                    tipo=tipo,
                    documento=doc,
                    nombre=name,
                    apellidos=last,
                    direccion='',
                    empresa_id=1)
            except:
                pass
class CargarUnidadesTrabajo:
    def __init__(self):
        self.df = read_excel(r"C:\inetpub\wwwroot\app\test\inf. Henry.xlsx",sheet_name='p. confianza',dtype=str)
    def cargar(self):
       
        # self.df.columns = self.df.iloc[1]
        # self.df = self.df.iloc[2:,:]
        dni = self.df['DNI'].to_list()
        empleado = self.df['APELLIDOS Y NOMBRES'].to_list()
        apellido,nombre =[],[]
        for em in empleado:
            date = em.split(' ')
            apellido.append(' '.join(date[:2]))
            nombre.append(' '.join(date[2:]))
        cargo = self.df['Posicion'].to_list()
        unidad = self.df['Unidad'].to_list()
        # self.unidad(unidad)
        # self.cargo(cargo,unidad)
        for doc,ap,name,car,un in zip(dni,apellido,nombre,cargo,unidad):
            print(doc)
            # u = UnidadTrabajo.objects.get(unidad=un.strip())
            c = CargoTrabajador.objects.get(cargo=car.strip())
            try:
                Trabajadores.objects.create(
                    tipo='1',
                    documento=str(doc).strip(),
                    nombre = name.strip(),
                    apellidos = ap.strip(),
                    cargo =c,
                    empresa_id=1

                    ).save()
            except:
                pass
    def unidad(self,unidad):
        for i in unidad:
            try:
                UnidadTrabajo.objects.create(unidad=i.strip()).save()
            except:
                pass
    def cargo(self,cargo,unidad):
      
        for i,j in zip(cargo,unidad):
            uni = UnidadTrabajo.objects.get(unidad=j.strip())
            print(uni.unidad)
            try:
                CargoTrabajador.objects.create(cargo=i.strip()).save()
            except Exception as e:

                print(e)
class cargarUnidades1:
    def __init__(self):
        self.df = read_excel(r"C:\inetpub\wwwroot\app\test\inf. Henry.xlsx",sheet_name='EMPLEADOS',dtype=str)
    def cargar(self):
        self.df.columns = self.df.iloc[1]
        self.df = self.df.iloc[2:,:]
        dni = self.df['DNI'].to_list()
        empleado = self.df['APELLIDOS Y NOMBRES'].to_list()
        apellido,nombre =[],[]
        for em in empleado:
            date = em.split(' ')
            apellido.append(' '.join(date[:2]))
            nombre.append(' '.join(date[2:]))
        cargo = self.df['Posicion'].to_list()
        unidad = self.df['Unidad'].to_list()
        self.unidad(unidad)
        self.cargo(cargo,unidad)
        try:
            for doc,ap,name,car,un in zip(dni,apellido,nombre,cargo,unidad):
                # u = UnidadTrabajo.objects.get(unidad=un.strip())
                c = CargoTrabajador.objects.get(cargo=car.strip())
                try:
                    Trabajadores.objects.create(
                        tipo='1',
                        documento=str(doc).strip(),
                        nombre = name.strip(),
                        apellidos = ap.strip(),
                        cargo =c,
                        empresa_id=1

                        ).save()
                except:
                    pass
        except:
            pass
    def unidad(self,unidad):
        for i in unidad:
            try:
                UnidadTrabajo.objects.create(unidad=i.strip()).save()
            except:
                pass
    def cargo(self,cargo,unidad):
        for i,j in zip(cargo,unidad):
            uni = UnidadTrabajo.objects.get(unidad=j.strip())
            try:
                CargoTrabajador.objects.create(cargo=i.strip()).save()
            except:
                pass

