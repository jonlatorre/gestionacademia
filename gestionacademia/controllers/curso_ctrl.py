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
##Cargamos los subcontroladores
from seleccionlibros_ctrl import SeleccionLibrosCtrl
##Cargamos las subvistas
from gestionacademia.views.seleccionlibros_view import SeleccionLibrosView


class CursoCtrl (Controller):

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
##        self.model.curso.set_curso(-1)
        tabla_libros=[dict(nombre='Titulo',dato=1),dict(nombre='ISBN',dato=2),dict(nombre='Editorial',dato=3),dict(nombre='Autor',dato=4)]
        tv_init(self.view['tv_libros_curso'],self.model.curso.tv_libros,tabla_libros)
        return

    # Non-public methods


    # GTK signals
    def on_guardar_activate(self,boton):
        print "Saliendo del curso guardando"
        self.model.curso.guardar()
        return
    def on_bt_salir_activate(self,widget):
        return
    def on_tv_libros_button(self, treeview, event):
        print "##Gestionamos el botón derecho (el 3º)"
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
                self.view['popup'].popup( None, None, None, event.button, time)
            else:
                print "Si no hay nada elegido..."
                self.view['popup'].popup( None, None, None, event.button, time)
            return True
        pass
    ##Señales del popup
    def on_anadir_libro(self,widget):
        print "añadimos un libro"
        v = SeleccionLibrosView(self.view) # pass GestionacademiaView as the parent
        c = SeleccionLibrosCtrl(self.model, v)
        v.run() # this runs in modal mode
        return

    def on_eliminar_libro(self,widget):
        print "Borramos un libro"
        id = get_tv_selected(self.view['tv_libros_curso'])
        self.model.curso.eliminar_libro(id)
        pass
    # Observed properties
    def register_adapters(self):
        self.adapt('curso.nombre','nombre')
        self.adapt('curso.examen','examen')
        self.adapt('curso.nivel','nivel')
        self.adapt('curso.precio','precio')
        self.adapt('curso.nota_aprobado','nota_aprobado')
    pass # End of class
