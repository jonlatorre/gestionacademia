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

class InputGruposView(View):
    
    """InputGruposView handles only the graphical representation of the
    application. The widgets set is loaded from a glade file.
    
    Public methods:
    run()
    
    """

    def __init__(self, parent=None, stand_alone=True):
        
        """Constructor for InputGruposView reads a graphical representation of
        the view from a glade file.
        
        parent: The name of the window that spawned this one
        stand_alone: If true, this view is a window unto itself. If not,
            it is embedded in another window.
        
        """
        
        # Look for the ui file that describes the ui.
        ui = os.path.join(_config.get_data_path(), 'ui', 'InputGrupos.ui')
        if not os.path.exists(ui):
            ui = None
        
        # Top window/widget check.
        if stand_alone: top_widget = 'input_grupos'
        else: top_widget = 'sw_scroller'
        
        View.__init__(self, builder=ui, parent=parent, top=top_widget)
        
        return

    # Public methods

    def run(self):
        
        """Display the InputGrupos window."""
        
        res = self['input_grupos'].run()
        self['input_grupos'].destroy()
        return res


    pass # End of class
