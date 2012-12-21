# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject

# Third party libary imports
from gtkmvc import Controller

# Local library imports


class BancoCtrl (Controller):
    
    """Handles signal processing and keeps the model and view aligned for an
    About MVC-O quadruplet.
    
    Public methods:
    register_view(view)
    
    """

    # Public methods

    def register_view(self, view):
        
        """
        view: The view managed by this controller.
        
        """
        return

    # Non-public methods

 
    # GTK signals
    def on_guardar_activate(self,boton):
        print "Saliendo del banco guardando"
        self.model.guardar()
        return
    def on_bt_salir_activate(self,widget):
        return
    # Observed properties
    def register_adapters(self):
        self.adapt('nombre','nombre')
        self.adapt('codigo','codigo')
        self.adapt('direccion','direccion')
        self.adapt('ciudad','ciudad')
        self.adapt('provincia','provincia')
        self.adapt('cp','cp')
    pass # End of class
