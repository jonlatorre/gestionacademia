
from icalendar import Calendar, Event
from datetime import datetime
from icalendar import UTC # timezone

import os
os.sys.path.append('/home/patataman/gestionacademia')

from gestionacademia.utils import _config
from sqlobject import *
from gestionacademia.models.database_model import *
from gestionacademia.utils._global import *



cal = Calendar()

cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
conversion = dict(lunes=0,martes=1,miercoles=2,jueves=3,viernes=4,sabado=5,domingo=6)

for c in Clase.select(Clase.q.profesorID!=None):
    try:
        print "Tenemos la clase",c
        inicio,fin = c.horario.split('-')
        try:
            h_inicio, m_inicio = inicio.split(':')
        except:
            h_inicio, m_inicio = inicio.split('.')
        try:
            h_fin, m_fin = fin.split(':')
        except:
            h_fin, m_fin = fin.split('.')
        event = Event()
        event.add('summary', 'Clase los %s de %s'%(c.dia_semana,c.grupo[0].nombre))
        from datetime import datetime
        d_i = datetime(2011,12,5+conversion[limpiar_tildes(c.dia_semana).lower().strip()],int(h_inicio),int(m_inicio),0,tzinfo=UTC)
        event.add('dtstart', d_i)
        event.add('dtend', datetime(2011,12,5+conversion[limpiar_tildes(c.dia_semana).lower().strip()],int(h_fin),int(m_fin),0,tzinfo=UTC))
        cal.add_component(event)
    except IndexError:
        print "fallo porque la clase no pertenece a ningun grupo!"
    except ValueError:
        print "Fallo por que la hora no esta bien formateada"
# print cal.as_string()

f = open('example.ics', 'wb')
f.write(cal.as_string())
f.close()
