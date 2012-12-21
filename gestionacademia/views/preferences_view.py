# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import os.path
import gtk

# Third party library imports
from gtkmvc import View

# Local library imports
from gestionacademia.utils import _config


class PreferencesView(View):
    
    """This handles only the graphical representation of the
    application. The widgets set is loaded from glade file.
    
    Public methods:
    run()
    
    """

    def __init__(self, parent=None, stand_alone=True):
        
        """Constructor for PreferencesView reads a graphical representation of
        the view from a glade file.
        
        parent: The name of the window that spawned this one
        
        """
        
        View.__init__(self, parent=parent)
        
        # Look for the ui file that describes the ui.
        ui = os.path.join(_config.get_data_path(), 
                          'ui', 
                          'PreferencesGestionacademiaDialog.ui')
        
        # Top window/widget check.
        if stand_alone: top_widget = 'preferences_gestionacademia_dialog'
        else: top_widget = 'vbox_dialog'
        
        View.__init__(self, builder=ui, parent=parent, top=top_widget)
        
        return

    def run(self):
        
        """Display the PreferencesGestionacademiaDialog window."""
        
        res = self['preferences_gestionacademia_dialog'].run()
        self['preferences_gestionacademia_dialog'].destroy()
        return res

    pass # End of class
