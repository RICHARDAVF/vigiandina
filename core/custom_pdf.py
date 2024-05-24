from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib.units import inch,mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

class Numeracion(Canvas):
    def __init__(self,*args,**kwargs):
        Canvas.__init__(self,*args,**kwargs)
        self.paginas = []
    def showPage(self):
        self.paginas.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        paginas = len(self.paginas)
        for state in self.paginas:
            self.__dict__.update(state)
            self.numeracion(paginas)
            Canvas.showPage(self)
        Canvas.save(self)
    def numeracion(self,numeros_pagina):
        self.drawRightString(204*mm,15*mm+(.2*inch),f"Pagina {self._pageNumber} de {numeros_pagina}")
class PDFControlAccesos:
    def __init__(self,filename,custom,data,request):
        super(PDFControlAccesos,self).__init__()
        self.filename = filename
        self.custom = custom
        self.data = data
        self.request = request
        self.story = []
    def generate(self):
        try:
            style = TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ("FONTSIZE",(0,0),(-1,-1),10),
                        ('SPLITBYROWSPAN', (0, 0), (-1, -1), 1)
            ])
            table = Table(data=self.data,repeatRows=1,style=style)
            self.story.append(table)
            print(self.request)
            file = SimpleDocTemplate(filename=self.filename,pagesize=letter)
            file.build(self.story,onFirstPage=self.custom,onLaterPages=self.custom,canvasmaker=Numeracion)
        except Exception as e:
            print(str(e))
            raise Exception(str(e))
