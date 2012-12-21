# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE


# Standard library imports
import os.path

# Third party library imports
from gtkmvc import Model

# Local library imports
from gestionacademia.utils import _config
from database_model import Alumno

class AboutModel (Model):

    """An almost empty model for the 'About' dialog. It has been added
    to show how models might be used to separate the logic. In the
    spirit of this tutorial, the usage of an observable property for
    the credits text is an exaggeration.

    Instance variables:
    credits

    """

    credits = ""
    num_alumnos_alta = 0
    num_alumnos_total = 0
    num_grupos = 0
    num_profesores = 0
    # Look for the ui file that describes the ui.
    credits_file = os.path.join(_config.get_data_path(), 'about')
    if not os.path.exists(credits_file):
        credits_file = None

    __observables__ = ("credits","num_alumnos_alta","num_alumnos_total","num_grupos")

    def __init__(self):

        """Constructor for AboutModel initialises the model with its parent
        class, then sets credits to the contents of a file.

        """
        Model.__init__(self)

        self.credits = open(self.credits_file, "r").read()
        alumnos = Alumno.select(Alumno.q.activo==True)
        self.num_alumnos_alta = alumnos.count()
        alumnos = Alumno.select()
        self.num_alumnos_total = alumnos.count()
        return

    pass # End of class

