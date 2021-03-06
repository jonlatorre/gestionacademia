# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject, gtk

# Third party libary imports
from gtkmvc import Controller

# Local library imports
from gestionacademia.utils._global import *


class AsistenciaCtrl (Controller):

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
##        self.model.cargar(-1)

        cb_init(self.view['cb_alumnos'],self.model.lista_alumnos,self.model.alumnoID)
        cb_init(self.view['cb_grupos'],self.model.lista_grupos,self.model.grupoID)
        self.view['confirmado'].set_active(self.model.confirmado)
        return
    ##Metdodo que habilita la edicion del combo alumno
    def habilitar_edicion_alumno(self):
        self.view['cb_alumnos'].set_button_sensitivity(gtk.SENSITIVITY_ON)

    # Non-public methods


    # GTK signals
    def on_guardar_activate(self,boton):
        ##print "Saliendo de la asistecia guardando"
        res = self.model.guardar()
        if res == 2:
            mostrar_aviso("Horario Impreso","Horario")
        return
    def on_bt_salir_activate(self,widget):
        return
    def on_cb_alumnos_changed(self, widget):
        id = cb_get_active(widget,self.model.lista_alumnos)
        ##print "Cambiando alumnosID a %s"%id
        self.model.alumnoID = id
    def on_cb_grupos_changed(self, widget):
        id = cb_get_active(widget,self.model.lista_grupos)
        ##print "Cambiando grupoID a %s"%id
        self.model.grupoID = id
##    def on_confirmado_toggled(self, widget):
##        if widget.get_active():
##            ##print "Vamos a pasar a confirmado!"
##            self.model.set_confirmado()
##        else:
##            ##print "Quitamos la confirmacion"
##            self.model.confirmado = False
##        return
    # Observed properties
    def on_bt_imp_horario_clicked(self, widget):
        print "Imprimimos el horario"
        self.model.imprimir_horario()
    def imp_notas_alumnos_1(self,widget):
        self.model.imprimir_notas(1)
        pass
    def imp_notas_alumnos_2(self,widget):
        self.model.imprimir_notas(2)
        pass
    def imp_notas_alumnos_3(self,widget):
        self.model.imprimir_notas(3)
        pass
    def register_adapters(self):
        #self.adapt('confirmacion')
        self.adapt('precio')
        self.adapt('metalico')
        self.adapt('factura')
        self.adapt('confirmado')
    pass # End of class
