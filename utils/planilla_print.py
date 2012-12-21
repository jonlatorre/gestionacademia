import os
os.sys.path.append('/home/patataman/Dropbox/Trabajo/gestionacademia')
from gestionacademia.models.grupo_model import *

a = GrupoModel()

a.cargar(17)
a.imprimir_planilla_notas(1)
