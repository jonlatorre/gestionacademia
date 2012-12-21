# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path
import new
import logging

# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

#Para generación de PDF
from gestionacademia.utils._imprimir import *

# Local library imports
##Importamos el modelo de BBDD
from database_model import Asistencia,Grupo,Alumno,Festivo,Nota
##Importamos los modelos de alumno y grupo para sacar la lista
from gestionacademia.models.alumno_model import AlumnoModel
from grupo_model import GrupoModel
from gestionacademia.models.nota_model import NotaModel

from gestionacademia.utils import _config
from gestionacademia.utils._global import *


class AsistenciaModel(Model):

    """Model del banco
    Metodos públicos:

    """
    a = None
    confirmado = False
    precio = str()
    factura = False
    metalico = False
    alumnoID = -1
    grupoID = -1
    __observables__ = ('confirmado','precio','factura','metalico')
    def __init__(self,id=-1):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.alumnoModel = AlumnoModel()
        self.grupoModel = GrupoModel()
        self.lista_grupos = self.grupoModel.lista
        ##FIXME hay que cambiar la lista de alumnos, por otra con nombre
        self.lista_alumnos = self.alumnoModel.combo_alumnos
        self.cargar(id)

    def set_alumno(self,id):
        """Funcion que establece el alumno para poder ver el combo cuando aun no existe la asistencia creada"""
        ##print "Estableciendo el alumno..."
        self.alumnoID=id
        return
    def set_grupo(self,id):
        ##print "Estableciendo el alumno..."
        self.grupoID=id
        return
    def set_confirmado(self):
        """Función que cambia a SI confirmado el alumno en el grupo y lanza los procesos necesario"""
        ##Si tenemos cargado el objeto de BBDD lo editamos en caliente!
        if self.a:
            self.a.confirmado = True
        self.confirmado = True
        ##FIXME llamar a imprimir horario!!!
        print "Imprimiendo horario..."
        self.imprimir_horario()
    def cargar(self,id):
        ##print "Cargando el Asistencia %i"%id
        if id == -1:
            ##print "Es nuevo, nada que cargar"
            return
        self.a = Asistencia.get(id)
        for variable in ['precio','id','confirmado','alumnoID','grupoID','factura','metalico']:
            ##print "Cargando variable %s co el valor %s"%(variable,getattr(self.a,variable))

            setattr(self,variable,getattr(self.a,variable))
        if self.precio == None:
            self.precio = ""
    def guardar(self):
        g = Grupo.get(self.grupoID)
        ##Cambiamos la , por . para que funcione la conversion a float
        if self.precio:
            self.precio = self.precio.replace(',','.')
        if self.a:
            self.a.precio = self.precio
            self.a.factura = self.factura
            self.a.metalico = self.metalico
            self.a.grupo = g
            self.a.alumno = Alumno.get(self.alumnoID)
            ##Si en la interfaz tenemos confirmado y en BBDD no, confirmamos la asistencia
            if ( self.confirmado and not self.a.confirmado):
                self.set_confirmado()
                return 2
            else:
                self.a.confirmado = self.confirmado
                return 1
        else:
            ##print "Creando Asistencia nuevo"
            ##FIXME comprobar si el grupo no está completo!
            if g.alumnos.__len__() >= g.num_max:
                logging.debug("Grupo completo!")
                mostrar_aviso("Grupo lleno","Grupo lleno")
                return -1
            self.a = Asistencia(alumno=Alumno.get(self.alumnoID),grupo=Grupo.get(self.grupoID),
                precio=self.precio,confirmado=self.confirmado,factura=self.factura,metalico=self.metalico)
            return 0
    def imprimir_horario(self):
        fichero = get_print_path('Horarios')+"/Horario_%s.pdf"%self.a.id
        print "Imprimiendo el horario %i en el fichero %s"%(self.a.id,fichero)
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        ##banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide_pequeno.png')
        ##img=Image(banner)
        ##story.append(img)
        ##Intro
        estilo = estiloHoja['BodyText']
        story.append(Spacer(0,30))
        cadena = "<para alignment=center><b>HORARIO</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Datos del docu: alumno, grupo, profes
        cadena = "Nombre del alumno: <b>%s %s %s</b>"%(self.a.alumno.nombre,self.a.alumno.apellido1,self.a.alumno.apellido2)
        story.append(Paragraph(cadena, estilo))
        cadena = "Grupo: <b>%s</b>"%self.a.grupo.nombre
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))

        ##Tabla con el horario
        tabla =[['Día','Horario','Aula','Profesor']]
        for c in self.a.grupo.clases:
            tabla.append([c.dia_semana,c.horario,"%s - %s"%(c.aula.numero,c.aula.piso),"%s"%(c.profesor.nombre)])

        t = Table(tabla)
        t.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        story.append(t)
        story.append(Spacer(0,10))
        ##Lista de libros
        cadena="Listado de libros:                                          "
        story.append(Paragraph(cadena, estilo))
        for l in self.a.grupo.curso.libros:
            #Si el autor es None lo ponemos a ""
            autor = l.autor and l.autor or ""
            cadena = "%s - %s"%(l.titulo,autor)+"%s - ISBN: %s"%(l.editorial,l.isbn)
            story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))

        ##Calendario
        cadena = "<para alignment=center><b>Calendario</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        tabla =[['Día','Comentario']]
        for d in Festivo.select(orderBy=["ano","mes","dia"]):
            if d.observaciones:
                observ = d.observaciones
            else:
                observ = ""
            if d.inicio:
                observaciones="Inicio del curso (%s)"%observ
            elif d.fin:
                observaciones="Fin del curso(%s)"%observ
            else:
                observaciones = d.observaciones
            tabla.append(["%s-%s-%s"%(str(d.dia).rjust(2,'0'),str(d.mes).rjust(2,'0'),d.ano),observaciones])
            #story.append(Paragraph(cadena, estilo))
        t = Table(tabla)
        #t.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        story.append(t)


        ##Pie de página
        ##cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        ##story.append(Paragraph(cadena, estilo))
        ##cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        ##story.append(Paragraph(cadena, estilo))
        ##story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=A4)
        doc.build(story)
        ##Lo mandamos a imprimir
        send_to_printer(fichero)
        return
    def imprimir_notas(self,trimestre):
        try:
            nm = NotaModel()
            print "La mandamos imprimir"
            nm.imprimir_nota(self.a, trimestre)
        except Exception,e:
            print "No hay nota aun!",e


    def lista_cargos_banco(self,concepto,lista,medio):
        """Devuelve el listado de cargos a realiar para la facturacion"""
        logging.debug("Vamos a generar la lista de cargos a pasar al banco. Cobramos con concepto %s y es medio mes? %s"%(concepto,medio))
        asistencias = []
        cargos = []
        ##Recogemos las asistencias, si no hay lista todas las que no paguen en metalico
        ## ni necesiten factura
        if len(lista)==0:
            debug("No tenemos ina lista así que buscamos todas las asistencias quea cobrar a traves del banco")
            for a in Asistencia.select(AND(Asistencia.q.confirmado==True,Asistencia.q.metalico==False,Asistencia.q.factura==False)):
                asistencias.append(a)
        ##Si hay lista solo las asistencias de los grupos listados
        else:
            for grupo in lista:
                for a in Asistencia.select(AND(Asistencia.q.confirmado==True,Asistencia.q.metalico==False,Asistencia.q.factura==False,Asistencia.q.grupoID==grupo)):
                    asistencias.append(a)
        #Para los alumnos que den problemas al generar el cargo (no tienen el banco bien, etc)
        listado_alumnos_problemas = []
        ##Convertimos las asistecias en cargos
        for a in asistencias:
            #debug("generando el cargo al alumno %s"%a.alumno.id)
            ##Si no tiene precio especial, cogemos el del curso/nivel
            if a.precio=="" or a.precio==None:
                ##Algunos cursos tiene el precio a 0 (porque se les cobra por trimestre o por lo que sea
                #debug("No tiene descuento")
                if a.grupo.curso.precio == 0:
                    ##Saltamos al siguiente, no generamos cargo si el precio es 0
                    continue
                else:
                    precio = a.grupo.curso.precio
            else:
                ##Cogemos el precio especial
                precio = a.precio
            #print "Comprobamos si es medio mes",medio
            if medio:
                precio = float(precio) / 2
            #debug("añadimos el alumno a la lista")

            try:
                cargos.append((a.alumno.id,"%s %s, %s"%(a.alumno.apellido1,a.alumno.apellido2,a.alumno.nombre),[a.alumno.banco.codigo,a.alumno.sucursal,a.alumno.dc,a.alumno.cuenta],precio,concepto))
            except:
                debug("ASISTENCIA: Error al generar el cargo al alumno %s"%a.alumno.id)
                listado_alumnos_problemas.append(str(a.alumno.id))
        debug("Comprobamos si ha habido errores")

        if not len(listado_alumnos_problemas) == 0:
            debug("ASISTENCIA: Como hemos tenido algun problema hacemos un raise")
            raise Exception(listado_alumnos_problemas)
        debug("Cargos Ok")
        return cargos

    def lista_facturar(self,medio=False):
        """Generamos el listado de cargos a cobrar con factura"""
        cargos = []
        ##Convertimos las asistecias en cargos
        for a in Asistencia.select(AND(Asistencia.q.confirmado==True,Asistencia.q.factura==True)):
            ##Si no tiene precio especial, cogemos el del curso/nivel
            if a.precio=="" or a.precio==None:
                precio = a.grupo.curso.precio
            else:
                precio = a.precio
            if medio:
                precio = precio / 2
            cargos.append(("%s, %s %s"%(a.alumno.nombre,a.alumno.apellido1,a.alumno.apellido2),precio))
        return cargos
    def lista_metalico(self,medio=False):
        """Generamos el listado de cargos a cobrar en metalico"""
        cargos = []
        for a in Asistencia.select(AND(Asistencia.q.confirmado==True,Asistencia.q.metalico==True)):
            ##Si no tiene precio especial, cogemos el del curso/nivel
            if a.precio=="" or a.precio==None:
                precio = a.grupo.curso.precio
            else:
                precio = a.precio
            if medio:
                precio = precio / 2
            cargos.append(("%s, %s %s"%(a.alumno.nombre,a.alumno.apellido1,a.alumno.apellido2),precio))
        return cargos

    pass # End of class
