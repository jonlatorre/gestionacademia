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
from gestionacademia.models.asistencia_model import AsistenciaModel
from gestionacademia.controllers.asistencia_control import AsistenciaCtrl
from gestionacademia.views.asistencia_view import AsistenciaView


class SeleccionAlumnosCtrl (Controller):
    
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
        tabla_seleccion_alumnos=[dict(nombre='Numero',dato=0),dict(nombre='Apellido1',dato=2),dict(nombre='Apellido2',dato=3),dict(nombre='Nombre',dato=4)]
        tv_init(self.view['tv_seleccion_alumnos'],self.model.alumno.lista_alumnos,tabla_seleccion_alumnos)
        
        return
    # Non-public methods
    
    # GTK signals
    def on_tv_seleccion_alumnos_row_activated(self,widget,*args):
        if  self.model.grupo.g.alumnos.__len__() >= self.model.grupo.g.num_max:
            print "Grupo lleno"
            mostrar_aviso("Grupo lleno","Grupo lleno")
            return -1
        id = get_tv_selected(widget)
        ##Comprobamos si está lleno
        v = AsistenciaView(self.view) # pass GestionacademiaView as the parent
        m = AsistenciaModel()
        m.set_alumno(id)
        m.set_grupo(self.model.grupo.g.id)
        c = AsistenciaCtrl(m, v)
        v.run()

        
        

        self.model.grupo.anadir_alumno(id)
    # Observed properties
    def register_adapters(self):
        pass
    pass # End of class
