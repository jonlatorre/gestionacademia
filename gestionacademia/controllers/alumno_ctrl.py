# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject
import gtk

# Third party libary imports
from gtkmvc import Controller
from gtkmvc.adapters import UserClassAdapter


# Local library imports
from gestionacademia.models.banco_model import BancoModel
from gestionacademia.models.asistencia_model import AsistenciaModel
from gestionacademia.controllers.asistencia_control import AsistenciaCtrl
from gestionacademia.views.asistencia_view import AsistenciaView
from gestionacademia.models.preferences_model import PreferencesModel
from gestionacademia.models.database_model import Banco
from gestionacademia.utils._global import *

class AlumnoCtrl (Controller):

    """Handles signal processing and keeps the model and view aligned for an
    About MVC-O quadruplet.

    Public methods:
    register_view(view)

    """

    # Public methods

    def register_view(self, view):
        self.bancos = BancoModel()
        self.preferences = PreferencesModel()
        ##Establecemos el valor del ToggleButton
        self.view['activo'].set_active(self.model.activo)
        ##Establecemos el modelo y el formato de combo de bancos
        cb_init(self.view['cb_bancos'],self.bancos.lista_bancos,self.model.bancoID)
        ##Para el autocompletado del codigo de banco
        completion = gtk.EntryCompletion()
        completion.set_model(self.bancos.lista_bancos)
        completion.set_text_column(2)
        self.view['banco_codigo'].set_completion(completion)

        completion.connect('match-selected', self.on_banco_match_selected)
        ##Establecemos el modelo y el formato de combo de provincias
        self.provincias = Provincias()
        cb_init(self.view['cb_provincia'],self.provincias,self.model.provincia)
        ##Formateando el tv de grupos:
        tabla_grupos=[dict(nombre='Nombre',dato=1),dict(nombre='Confirmado',dato=2),dict(nombre='Precio',dato=3),dict(nombre='Horario',dato=4)]
        tv_init(self.view['tv_grupos'],self.model.lista_grupos,tabla_grupos)
        return

    # Non-public methods
    def validar(self):
        if not self.model.sucursal == '' and self.bancos.validaCuenta(self.bancos.codigo,self.model.sucursal,self.model.dc,self.model.cuenta) != 0:
            mostrar_aviso("La cuenta bancaria introducido no es correcta","Cuenta incorrecta")
            return -1
        if self.model.dni == '' or self.model.dni == None :
            ##print "Campo DNI vacio, no lo validamos"
            pass
        else:
            if not self.model.validaNif() == 0:
                mostrar_aviso("El DNI introducido no es correcto","DNI")
                return -1
        try:
            self.model.validar()
        except ValueError as error:
            mostrar_aviso("Se ha producido el error: %s"%error,"Campos incorrectos")
            return -1
        return 0

    # GTK signals
    def on_guardar_activate(self,boton):
        if self.validar() == -1:
            return -1
        res = self.model.guardar()
        if res == -1:
            mostrar_aviso("No se ha podido crear el alumno nuevo, algún campo es erroneo o falta","Problema creando usuario")
        else:
            mostrar_aviso("Alumno guardado correctamente","OK")
            self.view['alumno_dialog'].destroy()
    def on_activo_toggled(self, widget):
        self.model.activo = widget.get_active()
    def on_factura_toggled(self, widget):
        self.model.factura = widget.get_active()
    def on_cb_bancos_changed(self, widget):
        banco_id = cb_get_active(widget,self.bancos.lista_bancos)
        banco_codigo =  cb_get_active(widget,self.bancos.lista_bancos,2)
        debug("El usuario a cambiado el banco a %s - %s"%(banco_id,banco_codigo))
        self.model.bancoID = banco_id
        self.bancos.cargar(self.model.bancoID)
        self.model.banco_codigo = banco_codigo
        self.view['banco_codigo'].set_text(ajustar(banco_codigo,4))
    def on_cb_provincia_changed(self, widget):
        self.model.provincia = cb_get_active(widget,self.provincias)
    def on_dni_focus_out_event(self,widget,event):
        pass
##        if self.model.validaNif() != 0:
##            mostrar_aviso("El DNI introducido no es correcto","DNI incorrecto")
##            widget.grab_focus()
##            return False
##        return False
    def on_cuenta_focus_out_event(self,widget,event):
##        if self.bancos.validaCuenta(self.model.bancoID,self.model.sucursal,self.model.dc,self.model.cuenta) != 0:
##            mostrar_aviso("La cuenta bancaria introducido no es correcta","Cuenta incorrecto")
##            widget.grab_focus()
##            return False
##        else:
##            return False
        return False

    ##Señales del tv de grupos y su menu
    def on_tv_grupos_row_activated(self, widget, *args):
        id=get_tv_selected(widget)
        v = AsistenciaView(self.view) # pass GestionacademiaView as the parent
        m = AsistenciaModel()
        m.cargar(id)
        c = AsistenciaCtrl(m, v)
        v.run()
        self.model.refrescar_lista_grupos()
        return
    def on_tv_grupos_button_press_event(self, treeview, event):
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor( path, col, 0)
            self.view['popup_grupos'].popup( None, None, None, event.button, time)
            return True
    def cambiar_confirmacion(self, widget):
        tv_widget = self.view['tv_grupos']
        id= get_tv_selected(tv_widget)
        ##FIXME esto hay que hacerlo a través del modelo de asistencia
        self.model.asistencia.cambiarConfirmacion(id)
        pass
    def quitar_grupo(self, widget):
        tv_widget = self.view['tv_grupos']
        id= get_tv_selected(tv_widget)
        self.model.eliminarAsistencia(id)
        pass
    def anadir_grupo(self, widget):
        if self.model.id == -1:
            print "Alumno sin guardar, hay que guardarlo antes de añadir un grupo!"
            if self.validar == -1:
                return -1
        res = self.model.guardar()
        if res == -1:
            mostrar_aviso("No se ha podido crear el alumno nuevo, algún campo es erroneo o falta","Problema creando usuario")
        else:
            ##Lanzamos el dialogo de asistencia de alumno a grupo
            v = AsistenciaView(self.view) # pass GestionacademiaView as the parent
            m = AsistenciaModel()
            m.set_alumno(self.model.id)
            c = AsistenciaCtrl(m, v)
            v.run()
            self.model.refrescar_lista_grupos()
        return
    ##Funcion que se ejecuta cuando el usuario selecciona un banco de desplegable de sugerencias
    def on_banco_match_selected(self,widget,tree_model,tree_iter):
        codigo = tree_model.get_value(tree_iter,2)
        banco_id = tree_model.get_value(tree_iter,0)
        debug("El usuario a elegido un codigo de banco %s con id %s"%(codigo,banco_id))
        cb_set_active(self.view['cb_bancos'],self.view['cb_bancos'].get_model(), banco_id)
        return
    def on_bt_salir_pressed(self,widget):
        self.view['alumno_dialog'].destroy()
        return -1
    ##señal para imprimir la matrícula
    def on_imp_matricula_clicked(self,widget):
		debug("Vamos a imprimir la matícula")
		self.model.imprimir_matricula()
    # Observed properties

    def register_adapters(self):
        self.adapt('id','id')
        for variable in self.model._lista_variables:
            if (variable == 'bancoID') or (variable == 'provincia'):
                ##Esta 2 no los adaptamos, las gestionamos por señales de los combos
                pass
            elif variable == 'dni':
                ##Fixme se podría cambiar esto a otro método con gestión de la validación
                self.adapt(variable)
##            elif variable == 'telefono1':
##                a = UserClassAdapter(self.model,'telefono1','get','set')
##                a.connect_widget(self.view["telefono1"])
##                self.adapt(a)
            else:
                ##debug("Adaptando la variable %s"%variable)
                self.adapt(variable)
    pass # End of class
