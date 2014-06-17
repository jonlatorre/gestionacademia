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

from database_model import Banco

import new

# Local library imports
from gestionacademia.utils._global import *

class BancoModel(Model):

    """Model del banco
    Metodos públicos:

    """
    b = None
    lista_bancos = ListStore(int, str, str)
    tv_bancos = ListStore(int, str, str)
    nombre = ""
    codigo = ""
    direccion = ""
    ciudad = ""
    provincia = ""
    cp = ""
    __observables__ = ('nombre','codigo','direccion','ciudad','provincia','cp')
    def __init__(self):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.rellenar_lista()
    def rellenar_lista(self):
##        print "Rellenando/refrescando los modelos del combo y tree"
        self.lista_bancos.clear()
        self.tv_bancos.clear()
        for b in Banco.select(orderBy=Banco.q.codigo):
            self.lista_bancos.append([b.id,"%s - %s"%(ajustar(b.codigo,4),b.nombre),ajustar(b.codigo,4)])
            self.tv_bancos.append([b.id,str(ajustar(b.codigo,4)),b.nombre])
        return
    def buscar(self,codigo):
        res = Banco.select(Banco.q.codigo==codigo)
        if not res.count == 0:
            ##Hemos encontrado! Lo carhgamos para tener sus datos
            self.cargar(res[0].id)
            return True
        else:
            print "banco no encontrado"
            return False
    def cargar(self,id):
        ##FIXME esto hay que arreglarlo!
        self.set_banco(id)
    def set_banco(self,id):
        if id == -1:
            print "Sin id es un banco nuevo?"
            self.b = None
            self.id = -1
            self.nombre = ""
            self.codigo = 0000
            self.direccion = ""
            self.ciudad = ""
            self.provincia = ""
            self.cp = 00000
        else:
            self.b = Banco.get(id)
            self.id = self.b.id
            self.nombre = self.b.nombre
            self.codigo = self.b.codigo
            self.direccion = self.b.direccion
            self.ciudad = self.b.ciudad
            self.provincia = self.b.provincia
            self.cp = self.b.cp
    def guardar(self):
        if self.b:
            self.b.nombre = self.nombre
            self.b.codigo = self.codigo
            self.b.direccion = self.direccion
            self.b.ciudad = self.ciudad
            self.b.provincia = self.provincia
            self.b.cp = self.cp
        else:
            self.b = Banco(nombre = self.nombre,codigo = self.codigo,direccion = self.direccion, ciudad = self.ciudad,provincia = self.provincia,cp = self.cp)
        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return
    def borrar(self):
        """Función qie borra el banco previamente cargado"""
        print "Borramos el banco de la BBDD"
        Banco.delete(self.id)
        self.rellenar_lista()
    def validaCuenta(self,banco,sucursal,dig_ctrl,cuenta):
        if sucursal == 0 or banco == 9999:
            return 0
        banco = self.ajustar(banco,4)
        sucursal = self.ajustar(sucursal,4)
        dig_ctrl = self.ajustar(dig_ctrl,2)
        cuenta = self.ajustar(cuenta,10)
        dig1 = self.digitoControl("00"+banco+sucursal)
        dig2 = self.digitoControl(cuenta)
        dc_calc = "%s%s"%(dig1,dig2)
        if dig_ctrl != dc_calc:
            ##print "no coincide"
            return -1
        else:
            ##print "Todo ok"
            return 0
    def digitoControl(self,cadena):
        """Función que calcula el digito de control de la parte banco o de la parte cuenta"""
        PESOS=[ 1, 2, 4, 8, 5, 10, 9, 7, 3, 6 ]
        suma = 0
        cadena = str(cadena)
        for i in range(0,len(str(cadena))):
            suma = suma + int(PESOS[i])*int(cadena[i])
        resto = 11 - (suma%11)
        if resto == 10:
            resto = 1
        if resto == 11:
            resto = 0
        return resto

    def ajustar(self,campo,longitud):
        """Función que ajusta con 0 a la iquierda el campo hasta la longitud deseada"""
        campo = str(campo)
        campo = '0'*(longitud-len(campo))+campo
        return campo
    pass # End of class
