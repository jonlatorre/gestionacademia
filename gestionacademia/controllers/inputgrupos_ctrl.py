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


class InputGruposCtrl(Controller):
    
	"""Handles signal processing and keeps the model and view aligned for an
	About MVC-O quadruplet.
	
	Public methods:
	register_view(view)
	
	"""
    
    # Public methods

	def register_view(self, view):
		print "Registrando la vista de input grupos.."
		self.view.show()
		return
        
    # Non-public methods
    
    # GTK signals
	def on_imprimir_clicked(self, widget):
		logging.debug("Vamos a imprimir etiquetas de grupos")
		grupos = []
		# Leemos el texto
		buffertext = self.view['text_grupos'].get_buffer()
		print buffertext
		lista_text = buffertext.get_text(buffertext.get_start_iter(),buffertext.get_end_iter())
		# Partimos el texto en elementos 
		lista = lista_text.split(' ')
		#Tratamos de convertir a integer cada entrada del texto
		for elemento in lista:
			try:
				#Si va bien la añadimos a la lista de grupos
				grupos.append(int(elemento))
			except:
				print "No hemos podido convertir a un numero el texto %s"%elemento
		print "Vamos a mandar la lista",grupos
		self.model.alumno.imprimir_etiquetas(False,None,grupos)
				
		
		return
		
		
	pass # End of class
