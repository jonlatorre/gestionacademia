# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENS
import os

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject
from gestionacademia.utils import _config
from gestionacademia.models.preferences_model import PreferencesModel


import new
import datetime

preferences = PreferencesModel()

BBDD=os.path.join(preferences.dbpath)
sqlhub.processConnection = connectionForURI('sqlite://'+BBDD)

class Banco(SQLObject):
    nombre = UnicodeCol()
    codigo = DecimalCol(size=4,precision=0,unique=True)
    direccion = UnicodeCol()
    ciudad = UnicodeCol()
    provincia = UnicodeCol()
    cp = DecimalCol(size=5,precision=0)

class Alumno(SQLObject):
    activo = BoolCol(default=1)
    nombre = UnicodeCol()
    apellido1 = UnicodeCol()
    apellido2 = UnicodeCol()
    telefono1 = DecimalCol(size=9,precision=0)
    fecha_nacimiento = DateCol()
    fecha_creacion = DateCol(default=DateTimeCol.now())
    banco = ForeignKey('Banco',cascade='null')
    ##Obligatorios si...
    sucursal = DecimalCol(size=4,precision=0,default=0000)
    dc = DecimalCol(size=2,precision=0,default=00)
    cuenta = DecimalCol(size=10,precision=0,default=0000000000)
    ##Apartir de aquí opcionales
    email = UnicodeCol(default="")
    dni = UnicodeCol(default="")
    telefono2 = DecimalCol(size=9,precision=0,default=0)
    direccion = UnicodeCol(default="")
    ciudad = UnicodeCol(default="")
    provincia = DecimalCol(size=2,precision=0,default=49)
    cp = UnicodeCol(default="")##DecimalCol(size=5,precision=0,default='')
    observaciones = UnicodeCol(default="")
    ##Otras entidades relacionadas
    grupos  = MultipleJoin('Asistencia')

class Asistencia(SQLObject):
    grupo = ForeignKey('Grupo',cascade='null')
    alumno = ForeignKey('Alumno',cascade='null')
    confirmado = BoolCol(default=0)
    factura = BoolCol(default=0)
    metalico = BoolCol(default=0)
    precio = UnicodeCol(default="")
    notas = MultipleJoin('Notas')
    faltas = MultipleJoin('Notas')

class Nota(SQLObject):
    asistencia = ForeignKey('Asistencia',cascade='null')
    trimestre = DecimalCol(size=1,precision=0)
    control1 = DecimalCol(size=3,precision=0,default="0")
    control1_baremo = DecimalCol(size=3,precision=0,default="0")
    control2 = DecimalCol(size=3,precision=0,default="0")
    control2_baremo = DecimalCol(size=3,precision=0,default="0")
    control3 = DecimalCol(size=3,precision=0,default="0")
    control3_baremo = DecimalCol(size=3,precision=0,default="0")
    grama = DecimalCol(size=3,precision=0,default="0")
    grama_baremo = DecimalCol(size=3,precision=0,default="0")
    expresion = DecimalCol(size=3,precision=0,default="0")
    expresion_baremo = DecimalCol(size=3,precision=0,default="0")
    lectura = DecimalCol(size=3,precision=0,default="0")
    lectura_baremo = DecimalCol(size=3,precision=0,default="0")
    comportamiento = UnicodeCol(length=1,default="R")
    tareas = UnicodeCol(length=1,default="C")



class Falta(SQLObject):
    asistencia = ForeignKey('Asistencia',cascade='null')
    mes = DecimalCol(size=1,precision=0)
    justificadas = DecimalCol(size=3,precision=0,default="0")
    faltas = DecimalCol(size=3,precision=0,default="0")

class Profesor(SQLObject):
    activo = BoolCol(default=1)
    nombre = UnicodeCol()
    apellido1 = UnicodeCol()
    apellido2 = UnicodeCol(default="")
    telefono1 = DecimalCol(size=9,precision=0,default=000000000)
    ##No obligatorios
    telefono2 = DecimalCol(size=9,precision=0,default=000000000)
    email = UnicodeCol(default="")
    dni = UnicodeCol(default="")
    fecha_nacimiento = DateCol()
    fecha_creacion = DateTimeCol.now()
    direccion = UnicodeCol(default="")
    ciudad = UnicodeCol(default="")
    provincia = DecimalCol(size=2,precision=0,default=12)
    cp = DecimalCol(size=5,precision=0,default=48901)
    observaciones = UnicodeCol(default="")
    clases = MultipleJoin('Clase')

class Aula(SQLObject):
    ##nombre = UnicodeCol()
    numero = DecimalCol(size=3,precision=0)
    piso = UnicodeCol()
    aforo = DecimalCol(size=3,precision=0,default=14)
    clases = MultipleJoin('Clase')

class Clase(SQLObject):
    dia_semana = UnicodeCol(default="")
    aula = ForeignKey('Aula',cascade='null')
    horario = UnicodeCol()
    ##no obligatorio
    profesor = ForeignKey('Profesor',cascade='null')
    grupo = RelatedJoin('Grupo')

class Curso(SQLObject):
    nombre = UnicodeCol()
    precio = FloatCol(default=100)
    ##No obligatorios
    examen = UnicodeCol(default="")
    nivel = UnicodeCol(default="")
    libros = RelatedJoin('Libro')
    nota_aprobado = FloatCol(default=50)

class Grupo(SQLObject):
    nombre = UnicodeCol()
    clases= RelatedJoin('Clase')
    curso = ForeignKey('Curso',cascade='null')
    alumnos = MultipleJoin('Asistencia')
    num_max = DecimalCol(size=2,precision=0,default=14) #El tamaño default no es lo mejor que esté aquí, pero bueno


##class Provincia(SQLObject):
##    nombre = UnicodeCol()
##    cp = DecimalCol(size=2,precision=0)

class Festivo(SQLObject):
    ano = DecimalCol(size=4,precision=0)
    mes = DecimalCol(size=2,precision=0)
    dia = DecimalCol(size=2,precision=0)
    inicio = BoolCol(default=0)
    fin = BoolCol(default=0)
    observaciones = UnicodeCol(default="")

class Libro(SQLObject):
    titulo = UnicodeCol()
    autor = UnicodeCol()
    isbn = UnicodeCol()
    editorial = UnicodeCol()
    cursos = RelatedJoin('Curso')

class Dia(SQLObject):
    nombre = UnicodeCol()

Banco.createTable(ifNotExists=True)
Alumno.createTable(ifNotExists=True)
Clase.createTable(ifNotExists=True)
Aula.createTable(ifNotExists=True)
Profesor.createTable(ifNotExists=True)
Clase.createTable(ifNotExists=True)
Curso.createTable(ifNotExists=True)
Grupo.createTable(ifNotExists=True)
Libro.createTable(ifNotExists=True)
Asistencia.createTable(ifNotExists=True)
Festivo.createTable(ifNotExists=True)
Dia.createTable(ifNotExists=True)
Nota.createTable(ifNotExists=True)
Falta.createTable(ifNotExists=True)

def inicializar_dias():
    Dia(id=0,nombre='Lunes')
    Dia(id=1,nombre='Martes')
    Dia(id=2,nombre='Miércoles')
    Dia(id=3,nombre='Jueves')
    Dia(id=4,nombre='Viernes')
    Dia(id=5,nombre='Sábado')
    Dia(id=6,nombre='Domingo')


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
        a = Alumno(nombre='Jon %s'%n,apellido1="latorre",apellido2='martinez',dni=generaNif(),direccion='hola',banco=b,telefono1='944333222',telefono2='666777888',email='nadie@gmail.com',ciudad='barakaldo',cp='48902',provincia=12,sucursal=3421,cuenta=666555432136,fecha_nacimiento=datetime.date(1979,05,06),observaciones="")

def inicializar_profesores():
    print "Vamos a crear 5 profesores"
    for n in range(1,6):
        p = Profesor(nombre='Profe %s'%n,apellido1="de tal",apellido2='pascual',dni='22223%s4T'%n,direccion='hola',\
            telefono1='944333222',email='nadie@gmail.com',ciudad='barakaldo',cp='48902',\
            provincia=5,fecha_nacimiento=datetime.date(1969,05,06),observaciones="")
def inicializar_aulas():
    print "Inicializando aulas"
    for n in range(1,5):
        miaula = Aula(numero=n,piso="primero",aforo=20)
    for n in range(1,5):
        miaula = Aula(numero=n,piso="segundo",aforo=27)

def inicializar_clases():
    print "Creamos una clase"
    for n in range(1,3):
        Clase(dia_semana="lunes",horario="8-9",aula=Aula.select()[n],profesor=Profesor.select()[n])
def inicializar_grupos():
    num=0
    curso = Curso.select()[num+2]
    unaclase = Clase.select()[num]
    otraclase = Clase.select()[num+1]
    print "creamos un grupo"
    g = Grupo(curso=curso,nombre="Grupo 1",num_max=14)
    print "Añadiendo alumnos al grupo %s"%g.nombre
    alumnos = Alumno.select()
    for num in range(0,5):
        c = Asistencia(alumno=alumnos[num],grupo=g)
        g.alumnos.append(c)
    for num in range(6,10):
        c = Asistencia(alumno=alumnos[num],grupo=g)
        c.confirmado = True
        g.alumnos.append(c)
    print "Añadimos unas clases"
    g.addClase = unaclase
    g.addClase = otraclase

def populate():
    print "Vamos a popular la BBDD"
    inicializar_bancos()
    inicializar_cursos()
    inicializar_profesores()
    inicializar_aulas()
    inicializar_alumnos()
    inicializar_clases()
    inicializar_grupos()
    dia = Festivo(ano=2010,mes=11,dia=01)

def generaNif():
    import random
    LETRAS='TRWAGMYFPDXBNJZSQVHLCKE'
    ##print "Generamos un NIF aleatorio"
    dni = random.randrange(10000000,99999999,1)
    letra = LETRAS[dni%23]
    nif = "%i%s"%(dni,letra)
    ##print nif
    return nif

if __name__=='__main__':
    print "Nos ejecutan en solitario"

    #inicializar_grupos()
    populate()
