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

from database_model import Festivo

import new

# Local library imports


class FestivoModel(Model):

    """Model del banco
    Metodos públicos:

    """
    lista = ListStore(int, int, int, int,str,str,str)
    id = -1
    ano = -1
    mes = -1
    dia = -1
    inicio = False
    fin = False
    Festivo = Festivo
    observaciones = ""
    __observables__ = ['ano','mes','dia','inicio','fin','observaciones']
    f = None

    def __init__(self):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.limpiar()
        self.rellenar_lista()
    def limpiar(self,fecha=None):
        self.id = -1
        if fecha:
            self.cargar_fecha(fecha)
        else:
            self.ano = 0
            self.mes = 0
            self.dia = 0
        self.inicio = False
        self.fin = False
        self.observaciones = ""
        self.f = None
    def rellenar_lista(self):
##        print "Rellenando/refrescando los modelos del combo y tree"
        self.lista.clear()
        for d in Festivo.select(orderBy=["ano","mes","dia"]):
            texto_inicio="---"
            texto_fin="---"
            if d.inicio:
                texto_inicio="Inicio del curso"
            if d.fin:
                texto_fin="Fin del curso"
            self.lista.append([d.id,d.ano,d.mes,d.dia,texto_inicio,texto_fin,d.observaciones])
        return
    def es_festivo(self, fecha):
        print "Comprobando si la fecha ya está en la base de datos"
        print fecha
        res = Festivo.select(AND(Festivo.q.ano==fecha[0],Festivo.q.mes==fecha[1],Festivo.q.dia==fecha[2]))
        ##print res.count()
        if res.count() == 1:
            print "Ya es festivo!"
            self.cargar(res.id)
            return res.id
        else:
            print "No es festivo"
            self.cargar(-1)
            self.cargar_fecha(fecha)
            return -1
    def cargar_fecha(self,fecha):
        ##Cargamos en las variables temporales la fecha
        self.ano=fecha[0]
        self.mes=fecha[1]
        self.dia=fecha[2]
    def cargar(self,id=1):
        if id == -1:
            print "Sin id es un día nuevo?"
            self.limpiar()
            return
        else:
            print "Cargando el dia %i"%id
            self.f = Festivo.get(id)
            self.id = self.f.id
            for variable in self.__observables__:
                setattr(self,variable,getattr(self.f,variable))
            self.id = self.f.id
    def borrar(self):
        """Función qie borra el festivo previamente cargado"""
        print "Borramos el festivo de la BBDD"
        Festivo.delete(self.id)
        self.rellenar_lista()
    def buscar_inicio_curso(self):
        res = Festivo.select(Festivo.q.inicio==True)
        if len(list(res)):
            self.cargar = res[0].id
            return True
        else:
            print "No se ha encontrado el inicio del curso"
            self.cargar(-1)
            return False

    def guardar(self):
        if self.id==-1:
            print "Creando Festivo nuevo"
            self.f = Festivo(ano=self.ano,mes=self.mes,dia=self.dia,inicio=self.inicio,fin=self.fin,observaciones=self.observaciones)
            print "Creado el festivo %i"%(self.f.id)
        else:
            print "Guardando el festivo %i"%(self.id)
            for variable in self.__observables__:
                setattr(self.f,variable,getattr(self,variable))

        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return
    def marcar_dias(self,cal):
        cal.freeze()
        for dia in Festivo.select():
            if dia.mes == cal.get_date()[1]:
                cal.mark_day(int(dia.dia))
        cal.thaw()
    pass # End of class
