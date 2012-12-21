# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports

# Third party imports
from gestionacademia.utils import _importer
from gtkmvc import Model
import ConfigParser
import os
# Local library imports
from gestionacademia.utils import _config


class PreferencesModel (Model):
    
    """An almost empty model for the 'Preferences' dialog. 
    
    """
    config = None
    nombre = ""
    razon = ""
    direccion = ""
    NIF = ""
    motor = ""
    dbpath = ""
    banco = ""
    oficina = ""
    dc = ""
    cuenta = ""
    lista_variables_general = ['nombre','razon','direccion','NIF']
    lista_variables_tecnicos = ['motor','dbpath']
    lista_variables_financieros = ['banco','oficina','dc','cuenta']
    #FIXME: It should provide an example of storing preferences in a database using SQLObject.

    def __init__(self):
        
        Model.__init__(self)
        self.config = ConfigParser.RawConfigParser()
        self.cargar()
        
    def cargar(self):
        self.config.read(os.path.join(_config.get_data_path(), 'config', 'gestionacademia.conf'))
        for variable in self.lista_variables_general:
            setattr(self,variable,self.config.get('general',variable))
        for variable in self.lista_variables_tecnicos:
            setattr(self,variable,self.config.get('tecnicos',variable))
        for variable in self.lista_variables_financieros:
            setattr(self,variable,self.config.get('financieros',variable))
    def guardar(self):
        """Guardamos todas las variables en el fichero de config"""
        for variable in self.lista_variables:
            self.config.set('general',variable,getattr(self,variable))
        for variable in self.lista_tecnicos:
            self.config.set('tecnicos',variable,getattr(self,variable))
        for variable in self.lista_financieros:
            self.config.set('financieros',variable,getattr(self,variable))
    # Non-public methods

    # Observed properties

    pass # end of class
