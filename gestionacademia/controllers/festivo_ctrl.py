# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject

# Third party libary imports
from gtkmvc import Controller

# Local library imports


class FestivoCtrl (Controller):
    
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
        ##self.model.limpiar()
        return

    # Non-public methods

 
    # GTK signals
    def on_guardar_activate(self,boton):
        print "Saliendo del festivo guardando"
        self.model.guardar()
        return
    def on_bt_salir_activate(self,widget):
        return
    # Observed properties
    def register_adapters(self):
        for variable in self.model.__observables__:
            self.adapt(variable)
    pass # End of class
