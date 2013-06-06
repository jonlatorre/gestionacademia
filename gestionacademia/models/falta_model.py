# -*- coding: utf-8 -*-
### BEGIN LICENSE
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
### END LICENSE


# Standard library imports
import os.path,os
from datetime import date
import logging
# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject
import new

# Local library imports
from gestionacademia.utils import _config
##Importamos el modelo de BBDD
from database_model import Falta,Asistencia,Grupo,Alumno
##Importamos los modelos de alumno y grupo para sacar la lista
from gestionacademia.models.alumno_model import AlumnoModel
from gestionacademia.models.grupo_model import GrupoModel
#Para generación de PDF
from gestionacademia.utils import _imprimir
from gestionacademia.utils._global import *
from gestionacademia.utils._imprimir import *

class FaltaModel(Model):

    """Model del banco
    Metodos públicos:

    """
    f = None
    id = -1
    asistenciaID = -1
    alumnoID = -1
    grupoID = -1
    mes = -1
    justificadas=0
    faltas=0
    __observables__ = ('justificadas','faltas')
    def __init__(self,id=-1):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.clear()

    def clear(self):
        logging.debug("Limpiando la falta")
        self.f = None
        self.id = -1
        self.asistenciaID = -1
        self.alumnoID = -1
        self.grupoID = -1
        self.mes = -1
        self.justificadas=0
        self.faltas=0
    def buscar(self):
        ##Buscamos la asistencia
        logging.debug( "Buscado la falta del alumno %i al grupo %i mes %i"%(self.alumnoID,self.grupoID,self.mes))
        if self.mes == -1 or self.alumnoID == -1 or self.grupoID == -1:
            ##Falta algún dato
            logging.debug( "Faltan datos!" )
            return -1
        res = Asistencia.select(AND(Asistencia.q.alumnoID==self.alumnoID,Asistencia.q.grupoID==self.grupoID))
        if len(list(res)):
            ##en base a la asistencia buscamos si hay una nota
            asis = res[0]
            res = Falta.select(AND(Falta.q.asistenciaID==asis.id,Falta.q.mes==self.mes))
            if len(list(res)):
                self.f = res[0]
                logging.debug( "Encontrada falta %i"%self.f.id)
            else:
                logging.debug( "Creando falta nueva" )
                self.f = Falta(asistencia=asis,mes=self.mes)
            self.id = self.f.id
            return 1
        else:
            logging.debug( "No hemos encontrado la asistecia, algo va mal!")
            self.clear()
            return -1
    def cargar(self):
        if not self.id == -1:
            logging.debug( "Ya tenemos el ID cargamos la falta" )
            self.f = Falta.get(self.id)
        elif self.buscar()==1:
            logging.debug( "Ya hemos editado esta falta antes, la cargamos" )
            for variable in self.__observables__:
                setattr(self,variable,getattr(self.f,variable))
            return 0
        else:
            logging.debug( "No podemos cargar!" )
            return -1
    def guardar(self):
        if self.mes==-1 or self.alumnoID == -1 or self.grupoID == -1:
            logging.debug( "No se puede guardar si no están definidos todos los cambos" )
            return -1
        logging.debug( "Guardando la Falta %i del alumno %i grupo %i mes %i"%(self.id,self.alumnoID,self.grupoID,self.mes) )
        for variable in self.__observables__:
            setattr(self.f,variable,getattr(self,variable))
        return
    def imprimir_cartas_mes(self,mes):
        num = 0
        for f in Falta.select(AND(Falta.q.mes==mes,Falta.q.faltas>3)):
            self.id = f.id
            self.cargar()
            if (not f.asistenciaID):
                logging.debug("No ha asistencia asociada a la falta, nos la saltamos")
                continue
            if date.today().year - self.f.asistencia.alumno.fecha_nacimiento.year < 19 :
                logging.debug("Es menor de edad porque ha nacido el %s, imprimimos carta"%self.f.asistencia.alumno.fecha_nacimiento.year)
                self.imprimir_carta_faltas()
                num += 1
        return num
    def imprimir_carta_faltas(self):
        ##Imprime la carta de faltas de la falta cargada
        hoy=date.today()
        ##FIXME esto debería ir a preferencias
        fichero = os.path.join(get_print_path('Faltas'),"Carta_%s-%s_%s.pdf"%(hoy.year,self.f.mes,self.f.asistencia.alumno.id))
        logging.debug( "Imprimiendo carta de faltas %i en el fichero %s"%(self.f.id,fichero) )
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        #banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
        #img=Image(banner)
        #story.append(img)
        story.append(Spacer(0,45))
        ##Aquí un estilo adecuado, alineado derecha, para ventanilla, etc
        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=right>%s %s %s</para>"%(self.f.asistencia.alumno.nombre,self.f.asistencia.alumno.apellido1,self.f.asistencia.alumno.apellido2)
        story.append(Paragraph(cadena, estilo))
        cadena = "<para alignment=right>%s</para>"%(self.f.asistencia.alumno.direccion)
        story.append(Paragraph(cadena, estilo))
        cadena = "<para alignment=right>%s %s</para>"%(self.f.asistencia.alumno.cp,self.f.asistencia.alumno.ciudad)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,200))
        ##Intro
        cadena = "<para alignment=center><b>FALTAS DE ASISTENCIA</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        ##Datos del docu: alumno, grupo, profes
        cadena = "La presente carta es para informarle de que el alumno <b>%s %s %s</b> ha faltado %s veces a las clases del grupo %s."%(self.f.asistencia.alumno.nombre,self.f.asistencia.alumno.apellido1,self.f.asistencia.alumno.apellido2,self.f.faltas,self.f.asistencia.grupo.nombre)
        story.append(Paragraph(cadena, estilo))


        cadena="Faltas de asistencia: %s de las cuales justificadas son %s"%(self.f.faltas,self.f.justificadas)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        story.append(Spacer(0,30))
        story.append(Spacer(0,30))

        cadena="<para alignment=center><b>Secretaria general</b></para>"
        story.append(Paragraph(cadena, estilo))
        ##Pie de página

        #cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        return
    def imprimir_lista_mes(self,mes):
        ##Imprime el listado de faltas del mes cargado en self.mes
        hoy=date.today()
        fichero = os.path.join(get_print_path('Faltas'),"faltas_%s-%s.pdf"%(hoy.year,mes))
        logging.debug( "Imprimiendo listado de faltas en el fichero %s"%(fichero) )
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        #banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
        #img=Image(banner)
        #story.append(img)
        ##Aquí un estilo adecuado, alineado derecha, para ventanilla, etc
        estilo = estiloHoja['BodyText']

        ##Intro
        cadena = "<para alignment=center><b>LISTADO DE FALTAS %s</b></para>"%nombre_mes(mes)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))

        ##Tabla con las faltas
        tabla_faltas =[['Numero','Apellidos, Nombre','Grupo','Faltas','Justificadas']]
        
        for f in Falta.select(Falta.q.mes==mes):
            ##FIXME esto deberia ir en la consula SQL
            if (f.justificadas>3 or f.faltas>3):
                ##print f.id
                logging.debug( "Tenemos la falta %s"%(f.id))
                if (not f.asistenciaID):
                    logging.debug("No ha asistencia asociada a la falta, nos la saltamos")
                    continue
                logging.debug( "relacionada con la asistencia %s"%(f.asistencia.id) )
                tabla_faltas.append([f.asistencia.alumno.id,"%s %s, %s"%(f.asistencia.alumno.apellido1,
                    f.asistencia.alumno.apellido2,f.asistencia.alumno.nombre,),f.asistencia.grupo.nombre,f.faltas,f.justificadas])

        t_faltas = Table(tabla_faltas)
        t_faltas.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        story.append(t_faltas)

        ##Pie de página

        #cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=A4)
        doc.build(story)
        send_to_printer(fichero)

    pass # End of class
