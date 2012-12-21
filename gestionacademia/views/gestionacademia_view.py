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
from gestionacademia.utils import _global


class GestionacademiaView (View):
    
    """This handles only the graphical representation of the
    application. The widgets set is loaded from glade file.
    
    Public methods:
    add_sub_view(subview, container, position)
    set_state(state)
    
    """

    def __init__(self):
        
        """Constructor for GestionacademiaView reads a graphical representation of
        the view from a glade file.
        
        """
        
        # Look for the ui file that describes the ui.
        ui_filename = os.path.join(_config.get_data_path(), 'ui', 'GestionacademiaWindow.ui')
        if not os.path.exists(ui_filename):
            ui_filename = None
        
        # Initialise the view.
        View.__init__(self, builder=ui_filename, top='gestionacademia_window')
        
        return

    pass # End of class
