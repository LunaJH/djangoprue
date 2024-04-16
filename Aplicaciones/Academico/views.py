from django.shortcuts import render, redirect
from .models import Curso
from django.contrib import messages
from .models import Diploma
from django.shortcuts import render
from django.template.loader import get_template
from django.views import View

import os
from io import BytesIO

import itertools
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.colors import pink, black, red, blue,green
from reportlab.lib.units import inch
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
this_path = os.getcwd() + '/polls'







# Create your views here.
class PDFView(View):
    def get(self, request, *args, **kwargs):
        # Crear un objeto HttpResponse con el tipo de contenido de PDF
        response = HttpResponse(content_type='application/pdf')

        # Establecer el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
# Crear el objeto PDF, usando el objeto HttpResponse como su "archivo"
        p = canvas.Canvas(response)

        # Agregar contenido al PDF
        p.drawString(100, 800, "Hola, este es un reporte en PDF.")
        p.drawString(100, 780, "Puedes personalizar esto según tus necesidades.")
        p.drawString(480,750,'01/07/2016')
        p.setFont('Helvetica-Bold',12)
        p.drawString(480,750,'15/11/2023')
        p.line(460,747,560,747)
        p.setFillColor(red)
        p.rect(0,2*inch,0.2*inch,0.3*inch, fill=1)
        #p.drawImage("http://127.0.0.1:8000/static/images/1.jpeg",250,450)
        p.setFont('Helvetica',22)
 # Cerrar el objeto PDF y finalizar la respuesta
        p.showPage()
        p.save()
        return response


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generar_diploma(curso):
    from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generar_diploma(curso):# Crear un buffer para almacenar el contenido del PDF
    buffer = BytesIO()

    # Crear un lienzo para dibujar en el PDF con orientación horizontal
    c = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))

    # Establecer el fondo de color amarillo suave
    c.setFillColorRGB(255/255, 255/255, 204/255)
    c.rect(0, 0, letter[1], letter[0], fill=True)

    # Encabezado en una fuente elegante y más grande
    c.setFont('Times-Bold', 36)
    c.setFillColor(colors.black)
    text = "CERTIFICADO DE FINALIZACIÓN"
    text_width = c.stringWidth(text, 'Times-Bold', 36)
    c.drawCentredString(letter[1] / 2, 650, text)

    # Espaciado
    c.drawString(30, 600, '')

    # Línea decorativa
    c.line(30, 590, letter[1] - 30, 590)

    # Espaciado
    c.drawString(30, 570, '')

    # Contenido del diploma en una fuente elegante
    c.setFont('Times-Bold', 24)
    textcertifica = "Se certifica que:"
    textcertifica_width = c.stringWidth(textcertifica, 'Times-Bold', 24)
    c.drawString((letter[1] - textcertifica_width) / 2, 540, textcertifica)

    # Espaciado
    c.drawString(30, 520, '')

    c.setFont('Times-Italic', 28)
    text = curso.nombre
    text_width = c.stringWidth(text, 'Times-Italic', 28)
    c.drawCentredString(letter[1] / 2, 490, text)

    # Espaciado
    c.drawString(30, 470, '')

    c.setFont('Times-Roman', 18)
    text = f'ha completado satisfactoriamente el curso. ¡Felicitaciones por este logro!'
    text_width = c.stringWidth(text, 'Times-Roman', 18)
    c.drawCentredString(letter[1] / 2, 450, text)

    # Espaciado
    c.drawString(30, 430, '')

    # Información adicional (créditos alineados a la derecha)
    c.setFont('Times-Roman', 16)
    text = f'Créditos obtenidos: {curso.creditos}'
    text_width = c.stringWidth(text, 'Times-Roman', 16)
    c.drawRightString(letter[1] - 30, 410, text)

    # Nueva página para posibles extensiones (horizontal)
    c.showPage()

    # Guardar el PDF generado
    c.save()

    # Obtener el contenido del PDF desde el buffer
    pdf = buffer.getvalue()

    # Cerrar el buffer
    buffer.close()

    # Devolver el contenido del PDF generado
    return pdf


def reporte(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={curso.nombre}_diploma.pdf'

    pdf_content = generar_diploma(curso)
    response.write(pdf_content)

    return response


def inicio(request):
    cursosListados = Curso.objects.all()
    #messages.success(request, '!Cursos Listados¡')
    return render(request,"gestionCursos.html", {"cursos": cursosListados})

def slider_imagenes(request):
    return render(request, 'slider_imagenes.html')

def mostrar_imagenes(request):
    imagenes = Imagen.objects.all()
    return render(request, 'mostrar_imagenes.html', {'imagenes': imagenes})

def diplomas(request):
    # Lógica para obtener los diplomas o información relacionada
    return render(request, 'diplomas.html')

def generar_diplomas_pdf(request):
    # Datos necesarios para el diploma
    nombre = "Nombre del Recipiente"
    descripcion = "Diploma de Excelencia"

    # Carga la plantilla HTML del diploma
    template = get_template('diplomas.html')
    context = {'nombre': nombre, 'descripcion': descripcion}

    # Renderiza el diploma como HTML
    html = template.render(context)

    # Crea un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="diplomas.pdf"'

    # Convierte el HTML a PDF
    pisa.CreatePDF(html, dest=response)

    return response

def ver_diploma(request, diploma_id):
    diploma = Diploma.objects.get(pk=diploma_id)
    return render(request, 'diplomas/diploma.html', {'diploma': diploma})


def registrarCurso(request):
    codigo=request.POST['txtCodigo']
    nombre=request.POST['txtNombre']
    creditos=request.POST['txtMateria']
    creditos=request.POST['NumCreditos']
    
    curso=Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    messages.success(request, '!Cursos Registrado¡')
    return redirect('/')

def edicionCurso(request, codigo):
    curso=Curso.objects.get(codigo=codigo)
    return render(request, "edicionCurso.html", {"curso":curso})

def editarCurso(request):
    codigo=request.POST['txtCodigo']
    nombre=request.POST['txtNombre']
    creditos=request.POST['NumCreditos']
    
    curso=Curso.objects.get(codigo=codigo)
    curso.nombre = nombre
    curso.creditos = creditos
    curso.save()
    
    messages.success(request, '!Cursos Actualizado¡')
    
    return redirect('/')

        
def eliminarCurso(request, codigo):
    curso=Curso.objects.get(codigo=codigo)
    curso.delete()
    
    messages.success(request, '!Cursos Eliminados¡')
    
    return redirect('/')

