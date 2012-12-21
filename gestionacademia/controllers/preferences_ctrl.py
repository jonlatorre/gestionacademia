# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports

# Third pary library imports
from gestionacademia.utils import _importer
from gtkmvc import Controller

# Local library imports


class PreferencesCtrl (Controller):
    
    """Handles signal processing and keeps the model and view aligned for a
    Preferences MVC-O quadruplet.
    
    Public methods:
    register_view(view)
    
    """

    # Public methods

    def register_view(self, view):
        
        """Load values from the model to set the initial state of the view.
        
        view: The view managed by this controller.
        
        """
        
        return

    # Non-public methods

    # GTK signals

    def _on_preferences_dialog_response(self, dlg, id):
        # Signal handler for the dialog's response
        
        return

    # Observed properties
    def register_adapters(self):
        self.adapt('nombre')
        self.adapt('razon')
        self.adapt('direccion')
        self.adapt('NIF')
        self.adapt('motor')
        self.adapt('dbpath')
        self.adapt('oficina')
        self.adapt('dc')
        self.adapt('cuenta')
    pass # End of class
