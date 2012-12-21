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

from database_model import Libro

import new

# Local library imports


class LibroModel(Model):

    """Model del banco
    Metodos públicos:

    """
    l = None
    lista = ListStore(int, str)
    tv = ListStore(int, str, str,str,str)
    titulo = str("")
    isbn = str("")
    editorial = str("")
    autor = str("")
    __observables__ = ('titulo','isbn','autor','editorial')
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
        for l in Libro.select():
            self.lista.append([l.id,l.titulo])
            self.tv.append([l.id,l.titulo,l.isbn,l.editorial,l.autor])
        return
    def cargar(self,id):
        print "Cargando el libro %i"%id
        if id == -1:
            print "Sin id es un libro nuevo?"
            self.l = None
            self.id = -1
            self.titulo = ""
            self.isbn = ""
            self.editorial = ""
            self.autor = ""
        else:
            self.l = Libro.get(id)
            self.id = self.l.id
            self.titulo = str(self.l.titulo)
            if self.l.isbn:
                self.isbn = str(self.l.isbn)
            else:
                self.isbn="--"
            if self.l.editorial:
                self.editorial = str(self.l.editorial)
            else:
                self.editorial = "--"
            if self.l.autor == None :
                self.autor = "--"
            else:
                self.autor = str(self.l.autor)
    def guardar(self):
        if self.id == -1:
            print "Creando libro nuevo"
            self.l = Libro(titulo = self.titulo,isbn = self.isbn,autor = self.autor, editorial = self.editorial)
        else:
            print "Guardando el libro %i %s"%(self.id,self.titulo)
            self.l.titulo = self.titulo
            self.l.isbn = self.isbn
            self.l.editorial = self.editorial
            self.l.autor = self.autor
        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return
    def borrar(self):
        """Función qie borra el libro previamente cargado"""
        print "Borramos el libro de la BBDD"
        Libro.delete(self.id)
        self.rellenar_lista()

    pass # End of class
