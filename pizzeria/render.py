#Código obtenido # DEBUG:
# https://codeburst.io/django-render-html-to-pdf-41a2b9c41d16

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


class Render:

    """ Resume: metodo que es invocado en View y se encarga de renderizar
                el template indicado por parametro con ayuda de la libreria XHTML2PDF"""
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path) #Obtener el template
        html = template.render(params)  #Renderizar la template
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response) #Convertir el template a PDF
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf') #Retornar el PDF o error si no se pudo renderizar
        else:
            return HttpResponse("Error Rendering PDF", status=400)
