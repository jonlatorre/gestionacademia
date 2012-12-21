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


class AboutView(View):
    
    """AboutView handles only the graphical representation of the
    application. The widgets set is loaded from a glade file.
    
    Public methods:
    run()
    set_text(text)
    show_vscrollbar(show)
    
    """

    def __init__(self, parent=None, stand_alone=True):
        
        """Constructor for AboutView reads a graphical representation of
        the view from a glade file.
        
        parent: The name of the window that spawned this one
        stand_alone: If true, this view is a window unto itself. If not,
            it is embedded in another window.
        
        """
        
        # Look for the ui file that describes the ui.
        ui = os.path.join(_config.get_data_path(), 'ui', 'AboutGestionacademiaDialog.ui')
        if not os.path.exists(ui):
            ui = None
        
        # Top window/widget check.
        if stand_alone: top_widget = 'about_gestionacademia_dialog'
        else: top_widget = 'sw_scroller'
        
        View.__init__(self, builder=ui, parent=parent, top=top_widget)
        
        return

    # Public methods

    def run(self):
        
        """Display the AboutGestionacademiaDialog window."""
        
        res = self['about_gestionacademia_dialog'].run()
        self['about_gestionacademia_dialog'].destroy()
        return res

    def set_text(self, text):
        
        """Set the text on label_text (gtk.Label) to text. 
        
        text: The text to display in a label.
        
        """
        
        self['label_text'].set_markup(text)
        return

    def show_vscrollbar(self, show=True):
    
        """Show or hide the scrollbar(s) on sw_scroller (gtk.ScrolledWindow). 
        
        show: Show or hide (boolean)
        
        """
        
        sw = self['sw_scroller']
        hpol, vpol = sw.get_policy()
        if show: 
            vpol = gtk.POLICY_ALWAYS
        else: 
            vpol = gtk.POLICY_NEVER
        sw.set_policy(hpol, vpol)
        return

    pass # End of class
