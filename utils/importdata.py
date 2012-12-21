# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE

import os, base64
from struct import unpack
os.sys.path.append(os.path.realpath(os.curdir))

from gestionacademia.utils import _config
from gestionacademia.utils import _config

mypath = _config.get_data_path()


import datetime
from sqlobject import *

from gestionacademia.models.database_model import *

def import_grupos():
    ##inicializar_profesores()
    print "Importando Grupos...."
    ##Cogemos el primer profesor
    p = Profesor.select()[0]
    fichero = 'documentacion/bbdd_18_02_2011/BBDD/FACAGRUP.DAT'
    f = open(fichero,'r')

    ##La primeta entrada no sirve
    f.read(380)
    cadena = f.read(380)
    while len(cadena):
        id =                int(cadena[0:3])
        status =            cadena[3:4]
        curso =             cadena[4:19].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        texto =             cadena[19:34].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        alumnos =           cadena[34:36]
        altas =             cadena[36:38]
        confir =            cadena[38:40]
        cuota =             cadena[40:44]
        lunes_a =           cadena[44:52]
        lunes_a_pi =        cadena[52:54]
        lunes_a_aula =      cadena[54:56]
        martes_a =          cadena[56:64]
        martes_a_pi =       cadena[64:66]
        martes_a_aula =     cadena[66:68]
        miercoles_a =       cadena[68:76]
        miercoles_a_pi =    cadena[76:78]
        miercoles_a_aula =  cadena[78:80]
        jueves_a =          cadena[80:88]
        jueves_a_pi =       cadena[88:90]
        jueves_a_aula =     cadena[90:92]
        viernes_a =         cadena[92:100]
        viernes_a_pi =      cadena[100:102]
        viernes_a_aula =    cadena[102:104]
        lunes_b =           cadena[104:112]
        lunes_b_pi =        cadena[112:114]
        lunes_b_aula =      cadena[114:116]
        martes_b =          cadena[116:124]
        martes_b_pi =       cadena[124:126]
        martes_b_aula =     cadena[126:128]
        miercoles_b =       cadena[128:136]
        miercoles_b_pi =    cadena[136:138]
        miercoles_b_aula =  cadena[138:140]
        jueves_b =          cadena[140:148]
        jueves_b_pi =       cadena[148:150]
        jueves_b_aula =     cadena[150:152]
        viernes_b =         cadena[152:160]
        viernes_b_pi =      cadena[160:162]
        viernes_b_aula =    cadena[162:164]
        gsb =               cadena[164:165]
        escue =             cadena[165:166]
        libr =              cadena[166:180]
        libr1 =             cadena[200:203]
        statusb =           cadena[203:204]
        etiqueta =          cadena[204:216]
        ultimo =            cadena[216:218]
    
##        print id,unichr(cuota)
##        print unpack('cccc',cuota)
##        print unpack('HH',cuota)
##        print cuota
##        print etiqueta,libr,libr1,escue,gsb
        ##Comprobamos si existe el curso
        if not (id==7 or id==128 or id==133 or id==136 or id==147):
            ##print "No queremos importar si no es uno de los que falta"
            continue
        print "Importando grupo %i"%id
        res= Curso.select(Curso.q.nombre==curso)
        if len(list(res)):
            cur = res[0]
        else:
            ##Añadimos el libro al curso, primero comprobamos si el libro existe
            res = Libro.select(Libro.q.titulo==texto)
            if res.count() == 0:
                lib = Libro(titulo=texto,autor="",isbn="",editorial="")
            else:
                lib = res[0]
            cur = Curso(nombre=curso)
##            print "Añadiendo libro %s a curso %s"%(texto,curso)
            cur.addLibro(lib)
        
       ## print id,curso
        g = Grupo(id=id,curso=cur,nombre=curso)
        
        ##Trabajamos con el horario
        for letra in ['a','b']:
            for dia in ['lunes','martes','miercoles','jueves','viernes']:
                horario=locals()[dia+"_"+letra]
                numero=locals()[dia+"_"+letra+'_aula']
                piso=locals()[dia+"_"+letra+'_pi']
                if horario!="        ":
                    ##print letra,dia,horario,numero,piso
                    ##Primero comprobamos si extiste el aula o hay que crearla
                    ##Hack para evitar un pete en el grupo 145
                    if numero == "  ":
                        numero=0
                    res= Aula.select(AND(Aula.q.numero==numero))
                    if len(list(res)):
                        aula = res[0]
                    else:
                        aula = Aula(numero=numero,piso=piso)
                    ##Finalmente añadimos la clase
                    g.addClase(Clase(dia_semana=dia,aula=aula,horario=horario,profesor=p))
        
##        print "--------------------"
        cadena = f.read(380)


def import_bancos():
    print "Importando Bancos...."

    fichero = 'documentacion/bbdd_18_02_2011/BBDD/FACABANC.DAT'
    f = open(fichero,'r')

    ##La primeta entrada no sirve
    f.read(125)
    cadena = f.read(125)
    while len(cadena):
        id =            int(cadena[0:4])
        nombre =        cadena[4:34].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        direccion =     cadena[34:64].strip()
        cp =            cadena[64:69].strip()
        poblacion =     cadena[69:99].strip()
        provincia =     cadena[99:119].strip()
        if cp == '     ' or cp == '':
            cp=00000
        res= Banco.select(Banco.q.codigo==id)
        if len(list(res)):
            ban = res[0]
            
            ban.nombre=nombre
            ban.cp=cp
            ban.ciudad=poblacion
            ban.provincia=provincia
        else:
            ##Si no existe lo creamos
##            print "Creando banco"
            ban = Banco(nombre=nombre,codigo=id,direccion=direccion,ciudad=poblacion,provincia=provincia,cp=cp)
    
        
        cadena = f.read(125)

def convertir_fecha(fecha):
    ano = int(fecha[0:4])
    mes = int(fecha[4:6])
    dia = int(fecha[6:8])
    return datetime.date(ano,mes,dia)


def import_alumnos():
    print "Importando Alumnos...."
    Alumno.dropTable()
    Alumno.createTable()
    Asistencia.dropTable()
    Asistencia.createTable()
    ##Banco(nombre="Metalico",codigo=0000,direccion="Gran Vía, 30-32",ciudad="Bilbao",provincia="bizkaia",cp="48009")
    fichero = 'documentacion/bbdd_18_02_2011/BBDD/FACAALUM.DAT'
    f = open(fichero,'r')

    ##La primeta entrada no sirve
    f.read(270)
    cadena = f.read(270)
    while len(cadena):
        id =            int(cadena[0:5])
        status =        cadena[5:6]
        nombre =        cadena[6:26].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        apellido1 =     cadena[26:46].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        apellido2 =     cadena[46:66].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        direccion =     cadena[66:106].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        poblacion =     cadena[106:126].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        provincia =     cadena[126:141].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        cp =            cadena[141:146].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        telefono =      cadena[146:155].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        relleno =       cadena[155:160]
        dni =           cadena[160:173].strip().lower().capitalize().decode('ISO8859').replace('¥','ñ')
        grupo =         cadena[173:176]
        fecha_nac =     cadena[176:184]
        banco =         cadena[184:188]
        sucursal =      cadena[188:192]
        dc =            cadena[192:194]
        cuenta =        cadena[194:204]
        falta =         cadena[204:212]
        fbaja =         cadena[212:220]
        especial =      cadena[220:221]
        descuento =     cadena[221:225]
        marca =         cadena[225:226]
        confirmado =    cadena[226:227]
        observaciones = cadena[227:247]
        filler =        cadena[247:269]
        
        cadena = f.read(270)
        ##De momento solo damos importamos los alumnos dados de alta
        if id == 72 and (marca == 'A' or marca == 'M'):
            ##Limpiando el telefono
            telefono = telefono.replace('-',"")
            telefono = telefono.replace('.',"")
##            print int(descuento)
            try:
                telefono = int(telefono)
            except:
                telefono=0
            ##print "Telefono %i"%telefono
            ##Puede que algunos campos estén vacios
            if banco == '    ':
                banco=0000
                sucursal=0000
                dc=00
                cuenta=0000000000
            if cp == '     ' or cp == '':
                cp=00000
            else:
                cp = int(cp)
            if dni == '             ' or dni == '':
                dni == "Sin Datos"
            else:
                ##Hay que limpiar el campo DNI quitando el -
                dni=dni.replace("-","")
            ##Cromprobamos si existe el banco
            res= Banco.select(Banco.q.codigo==banco)
            if len(list(res)):
                ban = res[0]
            else:
                ##Si no existe lo creamos
                print "Creando banco %s"%banco
                ban = Banco(nombre=str(banco),codigo=banco,direccion="",ciudad="",provincia="",cp="48009")
                
##            try:
            a=Alumno(id=id,nombre=nombre,apellido1=apellido1,apellido2=apellido2,
                telefono1=str(telefono),fecha_nacimiento=convertir_fecha(fecha_nac),banco=ban,
                ciudad=poblacion,direccion=direccion,sucursal=sucursal,cuenta=cuenta,dc=dc,
                dni=str(dni))
                
            ##Creando las asistencias
            asis = Asistencia(alumno=a,grupo=Grupo.get(grupo))
            if confirmado == "S":
                asis.confirmado=True
            if banco == '9999' or banco == '0' or banco == 0:
                print "%s paga en metalico"%a.id
                asis.metalico=True
##            except:
##                print "fallo creando el alumno %s %s %s :("%(nombre,apellido1,apellido2)
                
            
if __name__=='__main__':
    print "Somos main"
    #if input("Quieres importar los bancos?(1 -> Sí 0 -> No)"):
    ##import_bancos()
    #if input("Quieres importar los grupos?(1 -> Sí 0 -> No)"):
    ##import_grupos()
    #if input("Quieres importar los alumnos?(1 -> Sí 0 -> No)"):
    import_alumnos()
    
