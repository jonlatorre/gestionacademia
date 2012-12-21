# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject
import gtk 
# Third party libary imports
from gtkmvc import Controller

# Local library imports
from gestionacademia.utils._global import *

class SeleccionLibrosCtrl (Controller):
    
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

        ##Formateamos el TreeView de la lista de alumnos
        tabla_libros=[dict(nombre='Titulo',dato=1),dict(nombre='ISBN',dato=2),dict(nombre='Autor',dato=3),dict(nombre='Editorial',dato=4)]
        tv_init(self.view['tv'],self.model.libro.tv,tabla_libros)
        
        return
    # Non-public methods
    
    # GTK signals
    def on_tv_row_activated(self,widget,*args):
        id = get_tv_selected(widget)
        self.model.curso.anadir_libro(id)
    # Observed properties
    def register_adapters(self):
        pass
    pass # End of class
