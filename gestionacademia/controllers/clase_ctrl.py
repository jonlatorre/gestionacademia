# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject

# Third party libary imports
from gtkmvc import Controller

# Local library imports
from gestionacademia.utils._global import *


class ClaseCtrl (Controller):
    
    """Handles signal processing and keeps the model and view aligned for an
    About MVC-O quadruplet.
    
    Public methods:
    register_view(view)
    
    """

    # Public methods

    def register_view(self, view):
        
        """Loads the text from the model, then starts a timer to scroll it
        after 2.1 seconds.
        
        view: The view managed by this controller.
        
        """
        
        cb_init(self.view['cb_profesor'],self.model.profesor.lista_cb_profesores,self.model.clase.profesor)
        cb_init(self.view['cb_aula'],self.model.aula.lista,self.model.clase.aula)
        return

    # Non-public methods

 
    # GTK signals
    def on_guardar_activate(self,boton):
        print "Saliendo de la clase guardando"
        if self.model.clase.guardar() == 1:
            ##Si devuelve 1 es una clase nueva y hay que añadirla al grupo
            self.model.grupo.anadir_clase(self.model.clase.c)
        return
    def on_bt_salir_activate(self,widget):
        return
    def on_cb_aula_changed(self, widget):
        self.model.clase.aula = cb_get_active(widget,self.model.aula.lista)
    def on_cb_profesor_changed(self, widget):
        try:
            self.model.clase.profesor = cb_get_active(widget,widget.get_model())   
            print "Cambio en el profesor. Ahora es %s"%self.model.clase.profesor
        except:
            return
    # Observed properties
    def register_adapters(self):
        self.adapt('clase.dia_semana','dia_semana')
        self.adapt('clase.horario','horario')
    pass # End of class
