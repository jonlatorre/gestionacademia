# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path

# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

from database_model import Clase, Profesor, Aula, Grupo

import new

# Local library imports


class ClaseModel(Model):

    """Model de clase
    Metodos públicos:

    """
    c = None
##    lista = ListStore(int, str)
##    tv = ListStore(int, str, str,str,str)
    id = -1
    dia_semana = ""
    profesor = ""
    aula = ""
    horario = ""
    grupo = ""
    variables = ['dia_semana','profesor','aula','horario','grupo']
    __observables__ = ('dia_semana','profesor','aula','horario')
    def __init__(self):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
    def cargar(self,id):
        print "Cargando la clase %i"%id
        if id == -1:
            print "Sin id es una clase nueva?"
            self.c = None
            self.id = -1
            self.dia_semana = ""
            self.profesor = -1
            self.aula = -1
            self.grupo=-1
            self.horario = ""
        else:
            self.c = Clase.get(id)
            self.id = self.c.id
            self.dia_semana = self.c.dia_semana
            self.profesor = self.c.profesorID
            self.aula = self.c.aulaID
            self.horario = self.c.horario

    def guardar(self):
        if self.id == -1:
            print "Creando clase nueva"
            print self.dia_semana,self.profesor,self.aula,self.horario,self.grupo
            self.c = Clase(dia_semana=self.dia_semana,profesor=Profesor.get(self.profesor),aula = Aula.get(self.aula),horario=self.horario)
            return 1
        else:
            print "Guardando la clase %i"%(self.id)
            print "el profesor es %s"%self.profesor
            self.c.dia_semana = self.dia_semana.lower()
            self.c.horario = self.horario
            self.c.profesor = Profesor.get(self.profesor)
            self.c.aulaID = self.aula
            return 0





    pass # End of class
