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

from gestionacademia.models.preferences_model import PreferencesModel
from gestionacademia.utils._global import *

class ProfesorCtrl (Controller):

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
        self.preferences = PreferencesModel()
        ##Establecemos el valor del ToggleButton
        self.view['activo'].set_active(self.model.activo)
        ##Establecemos el modelo y el formato de combo de provincias
        self.provincias = Provincias()
        cb_init(self.view['cb_provincia'],self.provincias,self.model.provincia)


        return

    # Non-public methods
    def validar(self):
        try:
            self.model.validar()
        except ValueError as error:
            mostrar_aviso("Se ha producido el error: %s"%error,"Campos incorrectos")
            return -1
        return 0
    def comprobar_campos(self):
        print "Comprobando si los campos obligatorios están completos"
        ##Comprobamos que los campos oblitarios no estén vacios
        ## 2014-09-11 quitamos la validacion en este curso no usan esos datos
        #for variable in ['nombre','apellido1','telefono1','fecha_nacimiento']:
        #    if getattr(self.model,variable)=="":
        #        print "Campo %s vacio!"%variable
        #        return -1
        ##FIXME validar la fecha, el telefono, etc
        print "todos los campos OK"
        return 1
    # GTK signals
    def on_cb_provincia_changed(self, widget):
        self.model.provincia = cb_get_active(widget,self.provincias)

    def on_guardar_activate(self,boton):
        ##FIXME falta la validación de: fecha, telefono1,....
        if self.validar() == -1:
            return -1

        self.model.guardar()
        mostrar_aviso("Profesor guardado correctamente","OK")
        self.view['profesor_dialog'].destroy()

    def on_activo_toggled(self, widget):
        self.model.activo = widget.get_active()
    def on_bt_salir_pressed(self,widget):
        self.view['profesor_dialog'].destroy()
        return -1

    # Observed properties
    def register_adapters(self):
        for variable in self.model._lista_variables:
            self.adapt(variable)
    pass # End of class
