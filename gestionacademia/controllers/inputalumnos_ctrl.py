# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import gobject
import gtk 
import logging

# Third party libary imports
from gtkmvc import Controller

# Local library imports
from gestionacademia.utils._global import *


class InputAlumnosCtrl(Controller):
    
	"""Handles signal processing and keeps the model and view aligned for an
	About MVC-O quadruplet.
	
	Public methods:
	register_view(view)
	
	"""
    
    # Public methods

	def register_view(self, view):
		print "Registrando la vista de input alumnos.."
		self.view.show()
		return
        
    # Non-public methods
    
    # GTK signals
	def on_imprimir_clicked(self, widget):
		logging.debug("Vamos a imprimir etiquetas de alumnos")
		alumnos = []
		# Leemos el texto
		buffertext = self.view['text_alumnos'].get_buffer()
		print buffertext
		lista_text = buffertext.get_text(buffertext.get_start_iter(),buffertext.get_end_iter())
		# Partimos el texto en elementos 
		lista = lista_text.split(' ')
		#Tratamos de convertir a integer cada entrada del texto
		for elemento in lista:
			try:
				#Si va bien la añadimos a la lista de alumnos
				alumnos.append(int(elemento))
			except:
				print "No hemos podido convertir a un numero el texto %s"%elemento
		self.model.alumno.imprimir_etiquetas(False,alumnos)
				
		
		return
		
		
	pass # End of class
