# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path
import datetime
# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore
import datetime
from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

import new

#Pata generación de PDF
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# Local library imports
from database_model import Profesor
from gestionacademia.utils._global import *

def compara_horario(texto,hora):
    print texto
    inicio,fin = texto.split("-")
    inicio_hora,inicio_min = inicio.split(":")
    fin_hora,fin_min = fin.split(":")
    if (int(inicio_hora) >= hora) and  (hora <= int(fin_hora)):
        return "Ocupado"
    else:
        return "Libre"

class ProfesorModel (Model):

    """An almost empty model for the 'About' dialog. It has been added
    to show how models might be used to separate the logic. In the
    spirit of this tutorial, the usage of an observable property for
    the credits text is an exaggeration.
    Metodos públicos:
    set_Profesor
    guardar
    """
    time_format = "%Y-%m-%d" ##Declaramos el formato de la fecha de nacimiento como AÑO-MES-DIA
    a = None
    lista_profesores = ListStore(int, str, str, str,str)
    lista_cb_profesores = ListStore(int, str)
    lista_ocupacion = ListStore(str,str,str,str,str,str,str,str,str,str,str,str,str,str)
    id = -1
    lista_provincias = Provincias()
    provincia = 12
    _lista_variables=['activo','nombre','apellido1','apellido2','telefono1','telefono2','email','dni','fecha_nacimiento','fecha_creacion','direccion','ciudad','provincia','cp','observaciones']

    def __init__(self):

        """Constructor for AboutModel initialises the model with its parent
        class, then sets credits to the contents of a file.

        """
        Model.__init__(self)
        #self.rellenar_ocupacion()
        self.rellenar_lista()
    def imprimir_lista(self,todos=False):
        estiloHoja = getSampleStyleSheet()
        story = []
        cabecera = estiloHoja['Heading4']
        cabecera.pageBreakBefore=0
        cabecera.keepWithNext=0
        cabecera.backColor=colors.cyan
        parrafo = Paragraph("CABECERA DEL DOCUMENTO ",cabecera)
        story.append(parrafo)
        cadena = " Listado de Profesors"
        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)
        story.append(Spacer(0,20))

        tabla =[['nombre','apellido1','apellido2','telefono1','email','dni','fecha_nacimiento']]
        if todos:
            for persona in Profesor.select():
                tabla.append([persona.nombre,persona.apellido1,persona.apellido2,persona.telefono1,persona.email,persona.dni,persona.fecha_nacimiento])
        else:
            for persona in Profesor.select(Profesor.q.activo==True):
                tabla.append([persona.nombre,persona.apellido1,persona.apellido2,persona.telefono1,persona.email,persona.dni,persona.fecha_nacimiento])
        story.append(Table(tabla))
        doc=SimpleDocTemplate("listado_profesores.pdf",pagesize=A4,showBoundary=1)
        doc.build(story)
        send_to_printer(fichero)
        return

    def rellenar_ocupacion(self):
        for profesor in Profesor.select():
            self.lista_ocupacion.append(["Profesor","Dia",9,10,11,12,13,14,15,16,17,18,19,20])
            for profesor in Profesor.select():
                for dia in ["lunes","martes","miercoles","jueves","viernes"]:
                    horario = ""
                    for clase in profesor.clases:
                        if clase.dia_semana==dia:
                            horario = clase.horario.strip()
                            #print "Los %s tiene %s"%(dia,horario)
                            ocupacion_profesor = [profesor.nombre,dia]
                            for hora in [9,10,11,12,13,14,15,16,17,18,19,20]:
                                ocupacion_profesor.append(compara_horario(horario,hora))
                            lista_ocupacion.append(ocupacion_profesor)
                            
    def rellenar_lista(self,todos=False):
##        print "Rellenamos el treestore"
        self.lista_profesores.clear()
        if todos:
##            print "Nos piden TODOS los Profesors"
            for persona in Profesor.select():
                self.lista_profesores.append([persona.id,persona.dni,persona.apellido1,str(persona.telefono1),persona.nombre])
                self.lista_cb_profesores.append([persona.id,"%s %s,%s"%(persona.apellido1,persona.apellido2,persona.nombre)])
        else:
            for persona in Profesor.select(Profesor.q.activo==True):
                self.lista_profesores.append([persona.id,persona.dni,persona.apellido1,str(persona.telefono1),persona.nombre])
                self.lista_cb_profesores.append([persona.id,"%s %s,%s"%(persona.apellido1,persona.apellido2,persona.nombre)])

        return
    def cargar(self,id):

        if id == -1:
##            print "cargando datos vacios"
            for variable in self._lista_variables:
                try:
                    setattr(self,variable,'')
                except:
                    pass
            self.activo=1
            self.provincia=49
            self.id=-1
        try:
##            print "Cargando los datos del Profesor %i"%id
            self.a = Profesor.get(id)
            for variable in self._lista_variables:
                if (variable == 'fecha_nacimiento'):
                    ##La fecha nacimiento la pasamos a string
                    fecha = str(getattr(self.a,variable).isoformat())
                    self.fecha_nacimiento="%s"%fecha
                else:
                    setattr(self,variable,getattr(self.a,variable))
            self.id=id
        except:
            print "No hemos podido cargar el Profesor %s"%id
    def guardar(self):
        ##Comprobamos si existe el Profesor o es nuevo
        if self.id == -1:
            fecha_nac = datetime.datetime.strptime(self.fecha_nacimiento, self.time_format)
            print fecha_nac
            self.a = Profesor(nombre=self.nombre,apellido1=self.apellido1,\
                apellido2=self.apellido2,dni=self.dni,direccion=self.direccion,telefono1=int(self.telefono1),\
                telefono2=int(self.telefono2),email=self.email,ciudad=self.ciudad,cp=self.cp,provincia=self.provincia,\
                fecha_nacimiento=fecha_nac)
        else:
            for variable in self._lista_variables:
                if (variable == 'fecha_nacimiento'):
                    fecha = self.fecha_nacimiento
                    self.a.fecha_nacimiento = datetime.datetime.strptime(fecha, self.time_format)
                elif (variable=='fecha_creacion'):
                    ##La fecha de creación no se cambia
                    pass
                else:
                    setattr(self.a,variable,getattr(self,variable))
        ##en cualquier caso regeneramos la lista
        self.rellenar_lista()
    def borrar(self):
        """Función qie borra el profesor previamente cargado"""
        print "Borramos el profesor de la BBDD"
        Profesor.delete(self.id)
        self.rellenar_lista()
    def validar(self):
        """Función que valida los campos obligatorios antes de guardar"""
        if self.telefono2 == '':
            self.telefono2 = 0
        if self.apellido1=='':
            self.apellido1= '---'
        if self.apellido2=='':
            self.apellido2= '---'
        
        if self.nombre=='' :
            raise ValueError("Se debe rellenar nombre")
        #if not len(str(self.telefono1))==9:
        #    raise ValueError("El telefono debe tener 9 numeros")
        try:
            int(str(self.telefono1))
        except:
            #raise ValueError("El telefono debe tener solo numeros")
            self.telefono1=944937005
        if self.fecha_nacimiento == '':
            #raise ValueError("Falta la fecha nacimiento, recuerde que el formato es dia-mes-año")
            self.fecha_nacimiento = "1900-01-01"
        else:
            try:
                fecha = datetime.datetime.strptime(self.fecha_nacimiento, self.time_format)
            except:
                raise ValueError("Fecha nacimiento no valida, recuerde que el formato es dia-mes-año")
        if not len(str(self.cp))==5:
            #raise ValueError("El Código Postal debe tener 5 numeros")
            self.cp = 48980
            
        return True


    pass # End of class

