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

from database_model import Aula

import new

# Local library imports


class AulaModel(Model):
    
    """Model del banco
    Metodos públicos:

    """ 
    a = None
    lista = ListStore(int, str)
    tv = ListStore(int, str, str, str)
    aforo = ""
    numero = ""
    piso = ""
    __observables__ = ('aforo','numero','piso')
    def __init__(self):
        
        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.rellenar_lista()
    def rellenar_lista(self):
##        print "Rellenando/refrescando los modelos del combo y tree"
        self.lista.clear()
        self.tv.clear()
        for aula in Aula.select(orderBy='numero'):
            self.lista.append([aula.id,"%s - %s"%(aula.piso,aula.numero)])
            self.tv.append([aula.id,str(aula.numero),aula.piso,str(aula.aforo)])            
        return
    def cargar(self,id):
        print "Cargando el aula %i"%id
        if id == -1:
            self.a = None
            self.id = -1
            self.aforo = 14
            self.numero = 0
            self.piso = ""
        else:
            self.a = Aula.get(id)
            self.id = self.a.id
            self.aforo = self.a.aforo
            self.numero = self.a.numero
            self.piso = self.a.piso
        return
    def guardar(self):
        if self.id == -1:
            print "Creando aula nuevo"
            self.a = Aula(aforo = self.aforo,numero = self.numero,piso = self.piso)
            self.id = self.a.id
        else:
            print "Guardando el aula %i"%(self.id)
            self.a.aforo = self.aforo
            self.a.numero = self.numero
            self.a.piso = self.piso
        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return
    def borrar(self):
        """Función qie borra el aula previamente cargado"""
        print "Borramos el Aula de la BBDD"
        Aula.delete(self.id)
        self.rellenar_lista()
        return

    pass # End of class
