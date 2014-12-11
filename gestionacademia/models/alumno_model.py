# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path
import sys
import datetime
import re
# Third party library imports
from gtkmvc import Model, Observable
from gtkmvc.model import SQLObjectModel
from gtkmvc.adapters import UserClassAdapter

from gtk import ListStore
import datetime
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

import new
import csv

# Local library imports
from database_model import Alumno, Banco, Asistencia, Nota, Falta, Historia
from gestionacademia.utils import _config
from gestionacademia.utils._global import *
from gestionacademia.models.banco_model import BancoModel

#Para generación de PDF
from gestionacademia.utils._imprimir import *
#Para etiquetas
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter, A4

class PhoneClass(Observable):
    def __init__(self):
        Observable.__init__(self)
        self.telefono = 000000000
        return

    @Observable.observed
    def set(self,v):
        if not len(str(v))==9:
            raise ValueError("Longitud del campo telefono no adecuada")
        try:
            int(str(v))
        except:
            raise ValueError("El telefono solo puede contener números")
        self.telefono=v
    def get(self):
        return self.telefono
    pass


class AlumnoModel (Model):

    """Este es el modelo para los alumnos.
    Metodos públicos:
    cargar
    guardar
    imprimir_ista
    rellenar_lista
    validarNif
    """
    ##time_format = "%Y-%m-%d" ##Declaramos el formato de la fecha de nacimiento como AÑO-MES-DIA
    time_format = "%d-%m-%Y" ##Declaramos el formato de la fecha de nacimiento como DIA-MES-AÑO
    a = None
    ver_todos = False
    lista_alumnos = ListStore(int, str, str, str,str,bool,bool,str,str,str)
    lista_alumnos_filtro = lista_alumnos.filter_new()
    lista_alumnos_filtro.set_visible_column(5)
    combo_alumnos = ListStore(int, str)
    lista_grupos = ListStore(int,str,int,str,str)
    lista_historico = ListStore(int, str, str, str)
    id = -1
    telefono1 = PhoneClass()
    cuenta = 0
    dc=0
    sucursal=0
    bancoCodigo=0
    dni = ""
    alum_filtro_nomb = str("")
    alum_filtro_ape1 = str("")
    alum_filtro_ape2 = str("")
    
    _lista_variables=['activo','nombre','apellido1','apellido2','telefono1','telefono2','email','dni','fecha_nacimiento','fecha_creacion','direccion','ciudad','provincia','cp','bancoID','banco_codigo','sucursal','dc','cuenta','observaciones']
    def __init__(self):

        """Constructor for AlumnoModel initialises the model with its parent
        class, then fills up the alumn list.

        """
        Model.__init__(self)
        self.rellenar_lista()

    def rellenar_lista(self,todos=False):
        self.lista_alumnos.clear()
        self.combo_alumnos.clear()

        count = 0
        #debug("LA variable ver_todos tiene el valor %s"%self.ver_todos)
        if self.alum_filtro_nomb == "" and self.alum_filtro_ape1 == "" and self.alum_filtro_ape2 == "":
            if self.ver_todos==True:
                debug("Listamos todos los alumnos sin filtros")
                busqueda = Alumno.select()
            else:
                debug("Listamos todos los alumnos ACTIVOS sin filtros")
                busqueda = Alumno.select(Alumno.q.activo==True)
        else:
            if self.ver_todos==True:
                debug("Listamos los alumnos con los filtros: %s %s %s"%(self.alum_filtro_nomb,self.alum_filtro_ape1,self.alum_filtro_ape2))
                busqueda = Alumno.select(AND(Alumno.q.nombre.contains(self.alum_filtro_nomb),\
                                        Alumno.q.apellido1.contains(self.alum_filtro_ape1),\
                                        Alumno.q.apellido2.contains(self.alum_filtro_ape2)))
            else:
                debug("Listamos los alumnos ACTIVOS con los filtros: %s %s %s"%(self.alum_filtro_nomb,self.alum_filtro_ape1,self.alum_filtro_ape2))
                busqueda = Alumno.select(AND(Alumno.q.nombre.contains(self.alum_filtro_nomb),\
                                        Alumno.q.apellido1.contains(self.alum_filtro_ape1),\
                                        Alumno.q.apellido2.contains(self.alum_filtro_ape2),\
                                        Alumno.q.activo==True))
        for persona in busqueda:
            texto_clases = ""
            nombre_grupo = ""
            try:
                nombre_grupo = persona.grupos[0].grupo.nombre
                clases = persona.grupos[0].grupo.clases
                for clase in clases:
                    texto_clases = texto_clases + " %s-%s-aula %s-%s |"%(clase.dia_semana,clase.horario,clase.aula.piso,clase.aula.numero)
            except:
                ##NO hemos encontrados clase, que le vamos a hacer :)
                pass
            self.lista_alumnos.append([persona.id,persona.dni,persona.apellido1,persona.apellido2,persona.nombre,persona.activo,True,nombre_grupo,persona.telefono1,texto_clases])
            count += 1
            if persona.activo:
                self.combo_alumnos.append([persona.id,"%s - %s %s, %s"%(persona.id,persona.apellido1,persona.apellido2,persona.nombre)])
        debug("Hemos listado %s alumnos"%count)
        return

    def crear_pag_etiquetas(self,c,lista):
        sep_ancho = 110
        sep_alto = 37
        ##8 a la izquierda
        for num  in range(0,8):
            try:
                lista[num]
            except:
                break
            ancho = 8
            alto = sep_alto*(num)+20
            #print ancho,alto
            textobject = c.beginText()
            textobject.setTextOrigin(ancho*mm,alto*mm)
            textobject.setFont("Helvetica-Oblique", 14)
            for line in lista[num]:
                textobject.textLine(line)
            c.drawText(textobject)
        ## 8 a la derecha
        for num  in range(8,16):
            try:
                lista[num]
            except:
                break
            ancho =sep_ancho
            alto = sep_alto*(num-8)+20
            print ancho,alto
            textobject = c.beginText()
            textobject.setTextOrigin(ancho*mm,alto*mm)
            textobject.setFont("Helvetica-Oblique", 14)
            for line in lista[num]:
                textobject.textLine(line)
            c.drawText(textobject)

    def imprimir_etiquetas(self,todos=False,lista_alumnos_elegidos=None,lista_grupos_elegidos=None):
        """Función que imprime etiquetas con los datos de lso alumnos. Si todos es True imprime
        los alumnos dados de baja también"""
        lista = []
        p = Provincias()
        ##Preparamos el docu
        fichero = get_print_path('Alumnos')+"/Etiquetas_Alumnos.pdf"
        c = canvas.Canvas(fichero,pagesize=A4)
        c.translate(mm,mm)

        if todos:
            logging.debug("Imprimimos las etiquetas de todos los alumnos")
            busqueda = Alumno.select()
            
        elif lista_alumnos_elegidos!=None:
            logging.debug("Imprimimos solo ciertos alumnos")
            busqueda = []
            logging.debug(lista_alumnos_elegidos)
            for numero in lista_alumnos_elegidos:
                logging.debug( "Vamos a buscar el alumno %s"%numero)
                try:
                    busqueda.append(Alumno.get(numero))
                except:
                    logging.debug( "No hemos encontrado el alumno con la numero %s"%numero)
            
        elif lista_grupos_elegidos!=None:
            logging.debug("Imprimimos solo ciertos grupos")
            lista_alumnos_elegidos = []
            busqueda = []
            logging.debug(lista_grupos_elegidos)
            for numero in lista_grupos_elegidos:
                logging.debug("Buscando alumnos ne el grupo %s"%numero)
                for asistencia in Asistencia.select(Asistencia.q.grupoID==numero):
                    logging.debug("Añadiendo el alumno %s"%asistencia.alumno.id)
                    busqueda.append(asistencia.alumno)
            logging.debug(lista_alumnos_elegidos)
        else:
            logging.debug( "Imprimimos las etiquetas de los alumnos activos")
            busqueda = Alumno.select(Alumno.q.activo==True)
            
        for alumno in busqueda:
            i = p.get_iter_from_string(str(alumno.provincia))
            provincia = p.get_value(i,1)
            lista.append(["%s %s %s"%(alumno.nombre,alumno.apellido1,alumno.apellido2),"%s"%alumno.direccion,"%s - %s - %s"%(alumno.ciudad,alumno.cp,provincia)])
        ##Con la lista generada vamos a imprimir cada página con 16 etiquetas
        for x in range(0,len(lista),16):
            self.crear_pag_etiquetas(c,lista[x:x+16])
            c.showPage()
        ##Guardamos y listo!
        c.save()
        send_to_printer(fichero)
        return len(lista)

    def imprimir_lista(self,todos=False):
        fichero = get_print_path('Alumnos')+"/Listado_Alumnos.pdf"
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        ##banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
        ##img=Image(banner)
        ##story.append(img)

        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=center><b>LISTADO DE ALUMNOS</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))

        tabla =[['id','nombre','apellido1','apellido2','telefono1','dni','fecha_nacimiento']]
        if todos:
            for persona in Alumno.select(orderBy=Alumno.q.apellido1):
                tabla.append([persona.id,persona.nombre,persona.apellido1,persona.apellido2,persona.telefono1,persona.dni,persona.fecha_nacimiento])
        else:
            for persona in Alumno.select(Alumno.q.activo==True,orderBy=Alumno.q.apellido1):
                tabla.append([persona.id,persona.nombre,persona.apellido1,persona.apellido2,persona.telefono1,persona.dni,persona.fecha_nacimiento])
        t = Table(tabla)
        t.setStyle([('FONTSIZE',(0,0),(-1,-1),8),('FONTSIZE',(-1,0),(-1,-1),6),('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),('LINEBEFORE', (0,0), (0,-1), 2, colors.black),('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),('ALIGN', (1,1), (-1,-1), 'RIGHT')])
        story.append(t)
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        return
    
    def imprimir_lista_notas_asistencia(self,todos=False):
        """Pensado para una vez terminado el curso sacar un listado alfabetico 
        con las notas finales y el totald e faltas"""
        fichero = get_print_path('Alumnos')+"/Listado_Alumnos_Notas_Asistencia.pdf"
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        ##banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
        ##img=Image(banner)
        ##story.append(img)

        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=center><b>LISTADO DE ALUMNOS</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))

        tabla =[['Apellidos ','Nombre','Curso','Notal Final','Faltas','Justificadas']]
        if todos:
            consulta = Alumno.select(orderBy=Alumno.q.apellido1)
        else:
            consulta = Alumno.select(Alumno.q.activo==True,orderBy=Alumno.q.apellido1)
        for persona in consulta:
            #print "Estamos con la persona %s (%s) "%(persona.nombre,persona.id)
            nota_final = "----"

            #print "La asistencia es:",asis.id
            try:
                asis = persona.grupos[0]
                grupo = asis.grupo.nombre
            except:
                grupo = "-----"
            #print "El grupo es %s"%grupo
            notas = Nota.select(Nota.q.asistenciaID==asis.id)
            for nota in notas:
                #print "El trimestre %s"%nota.trimestre
                if nota.trimestre==3:
                    print "Estamos con la nota", nota.id
                    print nota
                    #~ ## primero comprobamos si es un pequeño coggemos la nota del 3º control, sino la de gramatica
                    #~ nombre_curso = grupo.lower()
                    #~ #FIXME esto debería ser una función externa
                    #~ if re.search('junior',nombre_curso) or re.search('beginner',nombre_curso) or re.search('movers',nombre_curso)  or re.search('starters',nombre_curso)  or re.search('flyers',nombre_curso):
                        #~ print "Es pequeño"
                        #~ nota_3trimestre = nota.control3
                        #~ baremo_3trimestre = nota.control3_baremo
                    #~ else:
                        #~ print "Es mayor"
                        #~ nota_3trimestre = nota.grama
                        #~ baremo_3trimestre = nota.grama_baremo
                    nota_3trimestre = nota.grama   
                    ### Buscamos la nota de grama, si es 0 cojemos el control3 si es 999 (no presentado ponemos un NP)
                    if nota_3trimestre == 0:
                        
                        nota_final = "NP"
                    elif nota_3trimestre == 999:
                        nota_final = "NP"
                    else:
                        nota_final = "%s /100"%(nota_3trimestre)
            total_faltas = 0
            total_faltas_j = 0
            try:
                for falta in Falta.select(Falta.q.asistenciaID==persona.grupos[0].id):
                    total_faltas = total_faltas + falta.faltas
                    total_faltas_j = total_faltas_j + falta.justificadas
            except:
                pass
            #except:
            #    print "Uo :( algún error"
            #    nota_final = "--"
            #    faltas = "--"
            ##Para los que solo tienen un apellido:
            try:
                apellidos = persona.apellido1+" "+persona.apellido2
            except:
                apellidos = persona.apellido1
            tabla.append([apellidos,persona.nombre,grupo,nota_final,total_faltas,total_faltas_j])
        t = Table(tabla)
        t.setStyle([('FONTSIZE',(0,0),(-1,-1),8),('FONTSIZE',(-1,0),(-1,-1),6),('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),('LINEBEFORE', (0,0), (0,-1), 2, colors.black),('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),('ALIGN', (1,1), (-1,-1), 'RIGHT')])
        story.append(t)
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        return

    def imprimir_matricula(self):
        from reportlab.platypus import ListFlowable, ListItem
        fichero = get_print_path('Alumnos')+"/Matricula_%s.pdf"%self.a.id
        print "Imprimiendo la matricula %i en el fichero %s"%(self.a.id,fichero)
        estiloHoja = getSampleStyleSheet()
        estiloHoja.add(ParagraphStyle(name='pie',
                              parent=estiloHoja['Normal'],
                              fontName = 'dejavu',
                              fontSize=6,
                              leading=6,
                              spaceAfter=2),
               alias='pie')
        estiloHoja.add(ParagraphStyle(name='normas',
                              parent=estiloHoja['Normal'],
                              fontName = 'dejavu',
                              fontSize=8,
                              leading=8,
                              spaceAfter=6),
               alias='normas')
        story = []
        ##Vamos con la cabecera
        ##banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide_pequeno.png')
        ##img=Image(banner)
        ##story.append(img)
        ##Intro
        cadena = "<para alignment=right> Numero Alumno: <b>%s</b> </para>"%self.id
        story.append(Paragraph(cadena,estiloHoja['Normal']))
        estilo = estiloHoja['BodyText']

        #story.append(Spacer(0,30))
        cadena = "<para alignment=center><b>Escuelas EIDE S.L. : Departamentos de Idiomas</b></para>"
        story.append(Paragraph(cadena, estiloHoja['Heading2']))
        story.append(Spacer(0,10))
        
        ##Datos del alumno
        
        tabla =[['Nombre',self.nombre,"Apellidos","%s %s"%(self.apellido1,self.apellido2)]]
        tabla.append(['fecha nacimiento',self.fecha_nacimiento,'Telefonos',"%s - %s"%(self.telefono1,self.telefono2)])
        tabla.append(["Domicilio:",self.direccion,"CP:",self.cp])
        tabla.append(["Poblacion:",self.ciudad,"DNI:",self.dni])
        tabla.append(["Como nos conocio:",self.observaciones, "email:",self.email])
        t = Table(tabla)
        story.append(t)
        story.append(Spacer(0,5))
        tablabajas =[['Fecha Renovación Curso 20__/__','Fecha Renovación Curso 20__/__','Fecha de baja']]
        tablabajas.append(['______________________________','______________________________','_____________'])
        tablabajas.append(['______________________________','______________________________','_____________'])
        tablabajas.append(['______________________________','______________________________','_____________'])
        tablabajas.append(['______________________________','______________________________','_____________'])
        tbajas = Table(tablabajas)
        story.append(tbajas)
        ##story.append(Spacer(0,5))
        
        ##Normas
        cadena = "<para alignment=center>NORMAS DEL CENTRO</para>"
        story.append(Paragraph(cadena, estiloHoja['Heading2']))
        estilo = estiloHoja['normas']
        normas = ListFlowable( [
        ListItem(Paragraph("""El alumno al formalizar la presente matrícula acepta las 
        condiciones siguientes:""", estilo)),
        ListItem(Paragraph("""La duración del curso es la estipulada 
        por la Dirección del Centro recogida en el calendario escolar que 
        se entrega a principios de curso.""",estilo)),
        ListItem(Paragraph("""En concepto de inscripción, y SOLO POR 
        UNA VEZ, se cobra una cantidad que no es susceptible de devolución 
        una vez entregada. Aquellos alumnos que causen baja en el Centro 
        antes de las fecha s fijadas como fin de curso en el Calendario 
        Escolar, serán considerados como Alumnos Nuevos si desean 
        reincorporarse al centro de nuevo, por lo que deberán abonar la 
        cuota de inscripción.""",estilo)),
        
        ListItem(Paragraph("""El curso se abonará por meses naturales 
        por adelantado (del 1 al 10 de cada mes) a través de domiciliación 
        bancaria.""",estilo)),
        
        ListItem(Paragraph("""La dirección del Centro se reserva el 
        derecho de cancelar las matrículas de aquellos alumnos cuya conducta 
        afecte desfavorablemente la marcha de las actividades del centro.""",estilo)),
        
        ListItem(Paragraph("""El Centro se reserva el derecho de cancelar 
        las clases de los grupos, cuyo número sea inferior a 4 alumnos.""",estilo)),
        
        ListItem(Paragraph("""No se reembolsará ninguna cantidad cuando 
        el alumno deje de asistir al curso o haya abonado algún importe del 
        mismo antes de su comienzo. El alumno tendrá que notificar su baja 
        en el centro antes del día 1 de cada mes, en caso contrario se cobrará 
        el recibo íntegro.""",estilo)),
        
        ListItem(Paragraph("""En el caso de devolución de recibo bancario, 
        el alumno abonará en caja el importe relativo a su curso más los 
        gastos que se hayan producido. No se admitirán devoluciones de 
        recibos una vez pasada una semana.""",estilo)),
        
        ListItem(Paragraph("""Tanto el equipamiento como el material 
        pedagógico de uso general de los alumnos es propiedad de EIDE, 
        y no deben, en ningún caso, ser retirados del centro.""",estilo)),
        
        ListItem(Paragraph("""La vigencia de la matrícula será para el 
        curso escolar contratado.""",estilo)),
        
        ListItem(Paragraph("""La matrícula quedará renovada si el alumno 
        entrega en Secretaría el documento de “renovación de matrícula” 
        que se distribuye en el mes de Mayo de cada año, siendo el coste 
        del curso el establecido en el listado de precios que corresponda 
        al nuevo curso escolar.""",estilo)),
        ])
        story.append(normas)
        ##Para firmar
        tabla =[['Conforme del Alumno','EIDE - Departamento de Idiomas'],['','']]
        
        t = Table(tabla)
        
        story.append(t)
        story.append(Spacer(0,35))
        ##LOPD Pie de página
        lopd = """Conforme a la L.O. 15/1999 de Protección de datos de carácter personal y su R.D. 1720/2007, los datos recabados serán incluidos en un fichero denominado clientes, inscrito en la Agencia de Protección de Datos, siendo su Responsable la empresa ESCUELAS INTERNACIONALES  PARA LA EDUCACION Y EL DESARROLLO EIDE , S.L. La finalidad de la obtención de los datos citados será exclusivamente la gestión de las actuaciones necesarias para la relación contractual. Vd., como titular de los datos, autoriza y consiente la inclusión de los mismos en el citado fichero. 
Los derechos de acceso, rectificación, cancelación y oposición serán ejercitables de manera gratuita dirigiéndose a ESCUELAS INTERNACIONALES  PARA LA EDUCACION Y EL DESARROLLO EIDE , S.L., con dirección: C/ Genaro Oraa nº6, C.P. 48980, Santurtzi, Bizkaia, indicando en la comunicación decisión referida a los derechos anteriormente mencionados.
"""
        story.append(Paragraph(lopd, estiloHoja['pie']))
        cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        story.append(Paragraph(cadena, estilo))
        cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        story.append(Paragraph(cadena, estilo))

        doc=SimpleDocTemplate(fichero,pagesize=A4)
        doc.build(story) 
        ##Lo mandamos a imprimir
        send_to_printer(fichero)
        send_to_printer(fichero)
        return

    def cargar(self,id):
        if id == -1:
            for variable in self._lista_variables:
                if variable == 'telefono1' or variable == 'telefono2' or variable == 'cp':
                    setattr(self,variable,0)
                try:
                    setattr(self,variable,'')
                except:
                    print "Error reiniciando %s"%variable
                    pass
            self.provincia=49
            self.banco = 2095
##            self.fecha_nacimiento="2010-03-03"
##            self.telefono1=555444333
##            self.telefono2=0
##            self.cp=48980
##            self.dni="22233444T"
            self.activo=1
            self.id=-1
            ##Limpiaos la lista de grupos
            self.lista_grupos.clear()
            self.lista_historico.clear()
        else:
            self.a = Alumno.get(id)
            for variable in self._lista_variables:
                if (variable == 'fecha_nacimiento'):
                    ##La fecha nacimiento la pasamos a string
                    ##fecha = str(getattr(self.a,variable).isoformat())
                    fecha = "%s-%s-%s"%(str(self.a.fecha_nacimiento.day),str(self.a.fecha_nacimiento.month),str(self.a.fecha_nacimiento.year))
                    self.fecha_nacimiento="%s"%fecha
                elif (variable == 'cuenta'):
                    setattr(self,variable,str(ajustar(getattr(self.a,variable),10)))
                elif (variable == 'dc'):
                    setattr(self,variable,str(ajustar(getattr(self.a,variable),2)))
                elif (variable == 'sucursal'):
                    setattr(self,variable,str(ajustar(getattr(self.a,variable),4)))
                elif (variable == 'banco_codigo'):
                    try:
                        setattr(self,variable,str(ajustar(self.a.banco.codigo,4)))
                    except:
                        setattr(self,variable,"9999")
                else:
                    setattr(self,variable,getattr(self.a,variable))
            self.id=id
            ##refrescamos la lista de grupos a los que quere asistir el alumno
            if self.email == None:
                self.email = "---"
            self.refrescar_lista_grupos()
            self.refrescar_lista_historico()
    def refrescar_lista_grupos(self):
        self.lista_grupos.clear()
        ##Cargamos la lista de grupos a traves de las asistencia, también si tiene descuento
        for asistencia in self.a.grupos:
            if asistencia.precio == None or asistencia.precio == "":
                precio = "Sin descuento"
            else:
                precio = float(asistencia.precio.replace(",","."))
            horario = ""
            for clase in asistencia.grupo.clases:
                horario += "%s-%s ; "%(clase.dia_semana,clase.horario)
            self.lista_grupos.append([asistencia.id,asistencia.grupo.nombre,asistencia.confirmado,precio,horario])
    def refrescar_lista_historico(self):
        self.lista_historico.clear()
        ##Cargamos la lista de grupos a traves de las asistencia, también si tiene descuento
        for evento in Historia.select(Historia.q.alumno==self.a):
            self.lista_historico.append([evento.id,"%s"%evento.fecha,evento.tipo,evento.anotacion])

    def guardar(self):
        self.cp = str(self.cp)
        if self.telefono2=='' or self.telefono2==0:
            debug("Falta telefono 2, lo ponemos a 000000")
            self.telefono2==000000000
        if self.sucursal == '':
            self.sucursal = 0
        if self.dc == '':
            self.dc = 0
        if self.cuenta == '':
            self.cuenta = 0
        ##Comprobamos si existe el alumno o es nuevo
        if self.id == -1:
            if self.bancoID=='':
                nuevo_banco = None
            else:
                nuevo_banco = Banco.get(self.bancoID)
            try:
                self.a = Alumno(nombre=self.nombre,apellido1=self.apellido1,\
                    apellido2=self.apellido2,dni=self.dni,direccion=self.direccion,\
                    banco=nuevo_banco,telefono1=self.telefono1,telefono2=self.telefono2,\
                    email=self.email,ciudad=self.ciudad,cp=self.cp,\
                    provincia=self.provincia,sucursal=self.sucursal,cuenta=self.cuenta,\
                    fecha_nacimiento=datetime.datetime.strptime(self.fecha_nacimiento, self.time_format),observaciones="")
                self.id = self.a.id
                debug("Guardando en el historico la creacion")
                h = Historia(alumno=self.a,tipo="creacion")
            except:
                print "Unexpected error:", sys.exc_info()[0],sys.exc_info()[1]
                return -1
        else:
            if self.activo == False:
                debug("El alumno está de baja")
                if self.a.activo == True: ## Si antes estaba dado de alta lo damos de baja
                    ## Creamo un evento en el historial
                    debug("Guardando en el historico la baja")
                    h = Historia(alumno=self.a,tipo="baja")
                    debug("Eliminado el alumno de los grupos")
                    for asis in self.a.grupos:
                        #~ print asis.grupo.nombre, asis.alumno.id
                        asis.destroySelf()
            else:
                print "El alumno está de alta"
                if self.a.activo == False: ## Si antes estaba dado de baja lo damos de alta
                    ## Creamo un evento en el historial
                    h = Historia(alumno=self.a,tipo="alta")
                    print "Dando de alta el alumno otra vez"
            for variable in self._lista_variables:
                if (variable == 'fecha_nacimiento'):
                    fecha = self.fecha_nacimiento
                    self.a.fecha_nacimiento = datetime.datetime.strptime(fecha, self.time_format)
                elif (variable=='fecha_creacion'):
                    ##La fecha de creación no se cambia
                    pass
                elif (variable=='bancoID'):
                    ##Comprobamos si el banco está definido, sino no hacemos nada
                    if self.bancoID:
                        self.a.banco = Banco.get(self.bancoID)
                    else:
                        pass
                else:
                    setattr(self.a,variable,getattr(self,variable))
                
            ##Regeneramos la lista
        self.rellenar_lista()
    def validar(self):
        """Función que valida los campos obligatorios antes de guardar"""
        if self.telefono2 == '':
            self.telefono2 = 0
        if self.nombre=='' or self.apellido1=='' or self.apellido2=='':
            raise ValueError("Se debe rellenar nombre y 2 apellidos")
        if not len(str(self.telefono1))==9:
            raise ValueError("El telefono debe tener 9 numeros")
        try:
            int(str(self.telefono1))
        except:
            raise ValueError("El telefono debe tener solo numeros")
        if self.fecha_nacimiento == '':
            raise ValueError("Falta la fecha nacimiento, recuerde que el formato es dia-mes-año")
        else:
            try:
                fecha = datetime.datetime.strptime(self.fecha_nacimiento, self.time_format)
            except:
                raise ValueError("Fecha nacimiento no valida, recuerde que el formato es dia-mes-año")
        if not len(str(self.cp))==5:
            raise ValueError("El Código Postal debe tener 5 numeros")
        return True
    def validaNif(self):
        if self.dni[0] == 'X' or self.dni[0] == 'Y' or self.dni[0] == 'x' or self.dni[0] == 'y':
            return 1
        LETRAS='TRWAGMYFPDXBNJZSQVHLCKE'
        nif = self.dni
        if nif.__len__() != 9:
            return -1
        dni = int(nif[:8])
        letra = nif[8].upper()
        if letra != LETRAS[dni%23]:
            return 1
        else:
            return 0
    def cambiarConfirmacion(self,id):
        asistencia = Asistencia.get(id)
        if not asistencia.confirmado:
            ##print "El alumno estaba sin confirmar, al confirmarlo generamos el horario..."
            ##FIXME
            ## impirmir horario
            asistencia.confirmado = True
            debug("Guardando en el historico la confirmacion")
            h = Historia(alumno=self.a,tipo="confirmacion",anotacion="Al grupo %s"%asistencia.grupo.nombre)
        else:
            asistencia.confirmado = False
        self.refrescar_lista_grupos()
    def eliminarAsistencia(self,id):
        asistencia = Asistencia.get(id)
        ##print "Vamos a borrar la asistencia de %s al grupo %s"%(asistencia.grupo.nombre,asistencia.alumno.nombre)
        Asistencia.delete(id)
        self.refrescar_lista_grupos()
    def comprobarCuentas(self,lista=[]):
        pendientes = []
        banco_model = BancoModel()
        #print "Tenemos la lista: %s"%lista
        if lista:
            debug("Como tenemos una lista de alumnos solo buscamos las cuentas de esos")
            lista = str(lista).strip('[').strip(']')
            debug("""id IN (%s)"""%lista)
            query = Alumno.select("""id IN (%s)"""%lista)
        else:
            debug("Como la lista está vacia comprobamos todos los alumnos")
            query = Alumno.select(Alumno.q.activo==True)
        for a in query:
            try:
                debug("Vamos a añadir al alumno %s - %s,%s"%(a.id,a.nombre,a.apellido1))
                if not a.grupos[0].metalico and not a.grupos[0].factura:
                    #debug("Intentando comprobar la cuenta del alumno %s"%a.id)
                    if a.sucursal == 0:
                        debug("Tiene la sucursal a 0!")
                        ##OJO solo funciona porque facturamos desde la BBK!!
                        if a.banco.codigo != 2095:
                            pendientes.append([a.id,"sucursal a 0"])
                        else:
                            debug("BBK y nos da igual que no valide la sucursal")
                    elif a.cuenta == 0:
                        pendientes.append([a.id,"cuenta a 0"])
                    elif banco_model.validaCuenta(a.banco.codigo,a.sucursal,a.dc,a.cuenta)!=0:
                        if a.banco.codigo != 2095:
                            pendientes.append([a.id,"no valida el DC"])
                        else:
                            debug("Es BBK y nos da igual que no valide el DC")
                    else:
                        pass
                else:
                    pass
            except:
                debug("A petado a si que algo estará mal")
                pendientes.append([a.id,"Otro error"])
        debug(pendientes)
        return pendientes
    
    def exportar_estadisticas_csv(self):
        file_name = get_print_path('Alumnos/')+'lista_usuarios.csv'
        with open(file_name, 'w+') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='E', quoting=csv.QUOTE_MINIMAL)
            for alumno in Alumno.select(Alumno.q.activo==True):
                try:
                    fila = ["%d"%alumno.id,"%s"%alumno.fecha_nacimiento,"%s"%alumno.fecha_creacion,\
                        "%s"%alumno.grupos[0].grupo.nombre.lower(),"%s"%alumno.grupos[0].grupo.curso.nombre.lower()]
                    #print fila
                except:
                    debug("No se ha podido leer información de alumno %d"%alumno.id)
                csvwriter.writerow(fila)
            csvfile.close()
        return file_name
    pass # End of class

