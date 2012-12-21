import os
os.sys.path.append('/home/patataman/Dropbox/Trabajo/gestionacademia')
from gestionacademia.models.grupo_model import *

a = GrupoModel()

a.cargar(126)
a.imprimir_planilla_asistencia(2010,12)
