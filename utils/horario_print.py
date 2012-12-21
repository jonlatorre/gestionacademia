import os
os.sys.path.append('/home/patataman/Dropbox/Trabajo/gestionacademia')
from gestionacademia.models.asistencia_model import *

a = AsistenciaModel()

a.cargar(1)
a.imprimir_horario()
