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

from database_model import Curso, Libro

import new

# Local library imports


class CursoModel (Model):

    """Modelo del curso.
    Metodos públicos:


    """
    c = None
    lista = ListStore(int, str, str, str, float,float)
    tv_libros = ListStore(int, str, str,str,str)
    nombre = ""
    examen = ""
    nivel = ""
    precio = 0
    nota_aprobado = 50
    solo_examen_final = False
    
    def __init__(self):
        """Constructor for CursoModel initialises the model with its parent
        class, then fills the liststore for the treeview.
        """
        Model.__init__(self)
        self.rellenar_lista()
    def rellenar_lista(self):
        self.lista.clear()
        for curso in Curso.select(orderBy=Curso.q.nombre):
            try:
                self.lista.append([curso.id,curso.nombre,curso.examen,curso.nivel,curso.precio,curso.nota_aprobado])
            except:
                pass
        return
    def rellenar_lista_libros(self):
        self.tv_libros.clear()
        for libro in self.c.libros:
            self.tv_libros.append([libro.id,libro.titulo,libro.isbn,libro.editorial,libro.autor])
    def cargar(self,id):
        print "Cargando el curso %i"%id
        if id == -1:
            print "Sin id es un curso nuevo?"
            self.c = None
            self.id = -1
            self.nombre = ""
            self.examen = ""
            self.nivel = ""
            self.precio = 100
            self.nota_aprobado = 50
            self.solo_examen_final = False
            self.tv_libros.clear()
        else:
            self.c = Curso.get(id)
            self.id = self.c.id
            self.nombre = self.c.nombre
            self.examen = self.c.examen
            self.nivel = self.c.nivel
            self.precio = self.c.precio
            self.nota_aprobado = self.c.nota_aprobado
            self.solo_examen_final = self.c.solo_examen_final
            self.rellenar_lista_libros()
        return
    def guardar(self):
        if self.id == -1:
            print "Creando curso nuevo"
            self.c = Curso(nombre = self.nombre,examen = self.examen,nivel = self.nivel, precio = self.precio, nota_aprobado = self.nota_aprobado,solo_examen_final=self.solo_examen_final)
            self.id = self.c.id
        else:
            print "Guardando el curso %i %s"%(self.id,self.nombre)
            self.c.nombre = self.nombre
            self.c.examen = self.examen
            self.c.nivel = self.nivel
            self.c.precio = self.precio
            self.c.nota_aprobado = self.nota_aprobado
            self.c.solo_examen_final = self.solo_examen_final
        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return
    def anadir_libro(self,id):
        ##obtenemos el libro
        milibro = Libro.get(id)
        print "Añadimos el libro %s"%milibro.titulo
        if self.c == None:
            ##Si no existe aun el curso, primero lo guardamos
            print "Antes guardamos el curso"
            self.guardar()
        self.c.addLibro(milibro)
        self.rellenar_lista_libros()
    def eliminar_libro(self,id):
        milibro = Libro.get(id)
        print "Eliminamos el libro %s"%milibro.titulo
        self.c.removeLibro(milibro)
        self.rellenar_lista_libros()
    def borrar(self):
        """Función que borra el curso previamente cargado"""
        print "Borramos el curso de la BBDD"
        Curso.delete(self.id)
        self.rellenar_lista()
    pass # End of class

