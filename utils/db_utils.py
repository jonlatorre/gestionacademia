#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENS
import os

os.sys.path.append('/home/patataman/Dropbox/Trabajo/gestionacademia')

from gestionacademia.utils import _config
mypath = _config.get_data_path()


import datetime
from sqlobject import *

from gestionacademia.models.database_model import *

def inicializar_cursos():
    print "Inicializamos la tabla de cursos con los datos buenos"
    Curso(nombre="Juniors 1", examen=None,nivel=None,precio=100)
    Curso(nombre="Juniors 2", examen=None,nivel='A1',precio=100)
    Curso(nombre="Juniors 3", examen=None,nivel='A1',precio=100)
    Curso(nombre="Juniors 4", examen=None,nivel='A1',precio=100)
    Curso(nombre="Begginers 1", examen=None,nivel='A1',precio=100)
    Curso(nombre="Begginers 1", examen=None,nivel='A1',precio=100)
    Curso(nombre="Begginers 1", examen=None,nivel='A2',precio=100)
    Curso(nombre="Begginers 1", examen='KET',nivel='A2',precio=100)
    Curso(nombre="Elementary Jov.", examen=None,nivel='A1',precio=140)
    Curso(nombre="Elementary Adu.", examen=None,nivel='A1',precio=140)
    Curso(nombre="Lower Intermediate Jov.", examen='KET',nivel='A2',precio=140)
    Curso(nombre="Lower Intermediate Adu.", examen='KET',nivel='A2',precio=140)
    Curso(nombre="Intermediate Jov.", examen='PET',nivel='B1',precio=140)
    Curso(nombre="Intermediate Adu.", examen='PET',nivel='B1',precio=140)
    Curso(nombre="Uper Intermediate Jov.", examen=None,nivel='B2',precio=140)
    Curso(nombre="Uper Intermediate Adu.", examen=None,nivel='B2',precio=140)
    Curso(nombre="First Certificate Jov.", examen='FCE',nivel='B2',precio=140)
    Curso(nombre="First Certificate Adu.", examen='FCE',nivel='B2',precio=140)
    Curso(nombre="Advance", examen='CAE',nivel='C1',precio=140)
    Curso(nombre="Proficiency", examen='CPE',nivel='C2',precio=140)
def inicializar_bancos():
    print "Creamos 2 bancos"
    b = Banco(nombre="BBK",codigo="2095",direccion="Gran Vía, 30-32",ciudad="Bilbao",provincia="bizkaia",cp="48009")
    b = Banco(nombre="Otra",codigo="2002",direccion="Gran Vía, 30-32",ciudad="Bilbao",provincia="bizkaia",cp="48009")

def inicializar_alumnos():
    print "Vamos a crear 20 alumnos"
    b = Banco.select()[0]
    for n in range(1,20):
        a = Alumno(nombre='Jon %s'%n,apellido1="latorre",apellido2='martinez',dni='3322223%s4T'%n,direccion='hola',banco=b,telefono='944333222',movil='666777888',email='nadie@gmail.com',ciudad='barakaldo',cp='48902',provincia='Bizkaia',sucursal=3421,cuenta=666555432136,fecha_nacimiento=datetime.date(1979,05,06),observaciones="")

def inicializar_horarios():
    print "Creamos un horario"
    unhorario = Horario(lunes_ho="8-9",lunes_cl="21",lunes_pf="Antonio")
    horario2 = Horario(lunes_ho="11-12",lunes_cl="23",lunes_pf="Julia")
    unhorario3 = Horario(martes_ho="8-9",martes_cl="21",martes_pf="Antonio")
#    print unhorario
def inicializar_grupos():
    num=0
    curso = Curso.select()[num+2]
    unhorario = Horario.select()[num] 
    print "creamos un grupo"
    g = Grupo(horario=unhorario,curso=curso,nombre="Grupo 1")
    print "Añadiendo alumnos al grupo %s"%g.nombre
    alumnos = Alumno.select()
    for num in range(0,5):
        c = Confirmacion(alumno=alumnos[num])
        g.addConfirmacion(c)
    for num in range(6,10):
        c = Confirmacion(alumno=alumnos[num])
        c.confirmado = True
        g.addConfirmacion(c)
#        g.alumnos.append(Confirmacion(alumnos[1],True))
#        g.alumnos.append(Confirmacion(alumnos[2],True))
#        g.alumnos.append(Confirmacion(alumnos[3],False))
#        g.alumnos.append(Confirmacion(alumnos[4],False))
#        g.alumnos.append(Confirmacion(alumnos[5],False))

def populate():
    print "Vamos a popular la BBDD"
    inicializar_bancos()
    inicializar_cursos()
    inicializar_alumnos()
    inicializar_horarios()
    inicializar_grupos()
    dia = Festivo(ano=2010,mes=11,dia=01)

if __name__=='__main__':
    print "Nos ejecutan en solitario"
    #inicializar_grupos()
    populate()



