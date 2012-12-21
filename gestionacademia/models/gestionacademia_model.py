# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Third part imports
from datetime import date
from gtkmvc import Model,ListStoreModel
import gtk
import gobject
import os
import logging
# Local library imports
##Modelos
from about_model import AboutModel
from alumno_model import AlumnoModel
from asistencia_model import AsistenciaModel
from grupo_model import GrupoModel
from profesor_model import ProfesorModel
from aula_model import AulaModel
from clase_model import ClaseModel
from banco_model import BancoModel
from curso_model import CursoModel
from libro_model import LibroModel
from festivo_model import FestivoModel
from nota_model import NotaModel
from falta_model import FaltaModel
from preferences_model import PreferencesModel
from facturacion_model import FacturacionModel
from database_model import *
##Otros
from gestionacademia.utils._imprimir import *
from gestionacademia.utils._global import *

class ListaMeses(ListStoreModel):
    id = -1
    nombre = ""
    def __init__(self):
        ListStoreModel.__init__(self,gobject.TYPE_INT,gobject.TYPE_STRING)
        self.insert(0,[0,''])
        id = 1
        for mes in ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre',]:
            self.insert(id,[id,mes])
            id += 1
        return



class GestionacademiaModel (Model):

    """This model contains references to other models that make up the
    application."""
    lista_meses = ListaMeses()
    lista_alumnos_grupo = gtk.ListStore(str)
    lista_trimestres = gtk.ListStore(int,str)
    facuracion = FacturacionModel()
    def __init__(self):
        Model.__init__(self)
        self.about = AboutModel()
        self.alumno = AlumnoModel()
        self.asistencia = AsistenciaModel()
        self.profesor = ProfesorModel()
        self.aula = AulaModel()
        self.clase = ClaseModel()
        self.grupo = GrupoModel()
        self.banco = BancoModel()
        self.curso = CursoModel()
        self.libro = LibroModel()
        self.festivo = FestivoModel()
        self.nota = NotaModel()
        self.falta = FaltaModel()
        self.facturacion = FacturacionModel()
        self.preferences = PreferencesModel()
        self.init_trimestres()
    def init_trimestres(self):
        self.lista_trimestres.append([1,"primero"])
        self.lista_trimestres.append([2,"segundo"])
        self.lista_trimestres.append([3,"tercero"])
    def facturar(self,lista=[],medio=False):
        ## "Buscamos las asistencia confirmadas, que no paguen en etalico ni necesiten factura"
        ##Pasamos los cobros...
        self.facturacion.nif = self.preferences.NIF
        for variable in ['banco','oficina','dc','cuenta']:
            setattr(self.facturacion,variable,getattr(self.preferences,variable))
        self.facturacion.sufijo = "000"
        texto = ""
        ##FIXME sacar la primera parte del concepto de la configuracion
        debug("Vamos a facturar %s"%self.facturacion.mes_cargo)
        try:
            debug("Generando el listado de cobros...")
            self.facturacion.lista_cobros = self.asistencia.lista_cargos_banco("CUOTA EIDE -  %s del %s"%(self.lista_meses[self.facturacion.mes_cargo][1],self.facturacion.ano_cargo),lista,medio)
        except Exception as e:
            debug("%No se ha generado la lista de cobros!")
            print e
            error = True
            return e,error

        ## si ha ido bien la generacion de los cargos creamos el fichero csb19
        fichero = os.path.join(get_print_path("Cobros"),"Recibo-%s-%s.dat"%(self.facturacion.ano_cargo,self.facturacion.mes_cargo))
        debug("llamamos a la generacion del fichero 19")
        self.facturacion.crear_fichero_19(fichero)
        debug("llamamos a la generacion de los listados")
        texto+= self.facturacion.listado_bancos()
        texto+= self.facturacion.listado_metalico(self.asistencia.lista_metalico(medio))
        texto+= self.facturacion.listado_facturar(self.asistencia.lista_facturar(medio))
        error = False
        return texto,error
    def limpiar_curso(self):
        print "Vamos a limpiar el curso..."
        print "Vamos con las notas..."
        for n in Nota.select():
            n.destroySelf()
            print ".",
        print "Vamos con las faltas..."
        print "---------"
        for f in Falta.select():
            f.destroySelf()
            print ".",
        print "---------"
        print "Pasamos todas las asistencias a no confirmadas..."
        for a in Asistencia.select():
            a.confirmado=False
            print ".",

    pass # End of class

