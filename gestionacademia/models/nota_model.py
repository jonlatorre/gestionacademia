# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path,os
from datetime import date
import re
# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject
import new

# Local library imports
from gestionacademia.utils import _config
from gestionacademia.utils._global import debug
##Importamos el modelo de BBDD
from database_model import Nota,Asistencia,Grupo,Alumno,Falta
##Importamos los modelos de alumno y grupo para sacar la lista
from gestionacademia.models.alumno_model import AlumnoModel
#from gestionacademia.models.grupo_model import GrupoModel
#Para generación de PDF
from gestionacademia.utils import _imprimir
from gestionacademia.utils._imprimir import *

def limpiar_nota(nota):
    """Función para la impresiónn que devuelve en blanco si la nota y el baremo son 0"""
    if nota==0:
        return 0
    elif nota==-1 or nota==999:
        return "NP"
    else:
        return nota

def convertir_comportamiento(comportamiento):
    conversion = {'M': "Malo", 'R': 'Regular', 'B':'Bueno', 'E':'Muy Bueno'}
    try:
        return conversion[comportamiento]
    except:
        return "-"

def convertir_tareas(tareas):
    conversion = {'N': "Nunca", 'P': 'Pocas Veces', 'A':'A Veces', 'C':'Casi Siempre', 'S': 'Siempre'}
    try:
        return conversion[tareas]
    except:
        return "-"


class NotaModel(Model):

    """Model del banco
    Metodos públicos:

    """
    n = None
    asistenciaID = -1
    alumnoID = -1
    grupoID = -1
    trimestre = -1
    #~ control1=int()
    #~ control1_baremo=int()
    #~ control2=int()
    #~ control2_baremo=int()
    #~ control3=int()
    #~ control3_baremo=int()
    grama=int()
    grama_baremo=int()
    expresion=int()
    expresion_baremo=int()
    lectura=int()
    lectura_baremo=int()
    fjustificadas=int()
    fnojustificadas=int()
    #~ tareas = str()
    #~ comportamiento = str()
    __observables__ = ('grama','grama_baremo','expresion','expresion_baremo','lectura','lectura_baremo')
    def __init__(self,id=-1):

        """Constructor for HorarioModel initialises the model with its parent
        class, then sets credits to the contents of a file.
        """
        Model.__init__(self)
        self.clear()

    def clear(self):
##        print "Limpiando"
        n = None
        asistenciaID = -1
        alumnoID = -1
        grupoID = -1
        trimestre = -1
        #~ control1=int()
        #~ control1_baremo=int()
        #~ control2=int()
        #~ control2_baremo=int()
        #~ control3=int()
        #~ control3_baremo=int()
        self.grama=int()
        self.grama_baremo=int()
        self.expresion=int()
        self.expresion_baremo=int()
        self.lectura=int()
        self.lectura_baremo=int()
        fjustificadas=int()
        fnojustificadas=int()
        #~ tareas = ""
        #~ comportamiento = ""
    def buscar(self):
        ##Buscamos la asistencia
        print "Buscado la nota del alumno %i al grupo %i trimestre %i"%(self.alumnoID,self.grupoID,self.trimestre)
        if self.trimestre == -1 or self.alumnoID == -1 or self.grupoID == -1:
            ##Falta algún dato
            return -1
        res = Asistencia.select(AND(Asistencia.q.alumnoID==self.alumnoID,Asistencia.q.grupoID==self.grupoID))
        if len(list(res)):
            ##en base a la asistencia buscamos si hay una nota
            asis = res[0]
            res = Nota.select(AND(Nota.q.asistenciaID==asis.id,Nota.q.trimestre==self.trimestre))
            if len(list(res)):
                self.n = res[0]
                print "Encontrada nota %i"%self.n.id
            else:
                print "Creando nota nueva"
                self.n = Nota(asistencia=asis,trimestre=self.trimestre)
                print "Creada",self.n
            self.id = self.n.id
            return 1
        else:
            print "No hemos encontrado la asistecia, algo va mal!"
            self.clear()
            return -1
    def cargar(self):
        ##ATENCION: antes hay que establecer las propiedades alumnoID,grupoID y trimestre
        if self.buscar()==1:
            print "Cargando las Notas"
            print self.__observables__
            for variable in self.__observables__:
                print "Cargando variable %s con el valor %s"%(variable,getattr(self.n,variable))
                setattr(self,variable,getattr(self.n,variable))
        else:
            print "No podemos cargar la nota!"
            return
    def guardar(self):
        ##FIXME cambiar este if y poner una sola instacia de setattr
        if self.trimestre==-1 or self.alumnoID == -1 or self.grupoID == -1:
            print "No se puede guardar si no están definidos todos los cambos"
            return -1
        print "Guardando la Nota %i del alumno %i grupo %i trimestre %i"%(self.n.id,self.alumnoID,self.grupoID,self.trimestre)
        for variable in self.__observables__:
            print "Guardando %s con el valor %s"%(variable,getattr(self,variable))
            setattr(self.n,variable,getattr(self,variable))
        return
    def imprimir(self,id):
        print "Imprimiendo las notas del trimestre %s"%id
        num_notas=0
        for n in Nota.select(Nota.q.trimestre==id):
            num_notas+=1
            mostrar_aviso("Funcion deshabilitada","Funcion deshabilitada")
            #self.imprimir_nota(n)

        return num_notas
    def imprimir_nota(self,asistencia,trimestre_imprimir):
        hoy=date.today()
        ##FIXME esto debería ir a preferencias
        fichero = os.path.join(_imprimir.get_print_path('Notas'),"nota_%s_%s.pdf"%(hoy.year,asistencia.alumno.id))
        debug("Imprimiendo las notas de la asistencia  %i en el fichero %s"%(asistencia.id,fichero))
        ##Vamos a intentar cargar todas las notas del alumno en los tres trimestres
        notas_trimestres = {}
        for trimestre in 1, 2, 3:
            notas = {}
            res = Nota.select(AND(Nota.q.asistenciaID==asistencia.id,Nota.q.trimestre==trimestre))
            if len(list(res)):
                n = res[0]
                #print "Encontrada nota %i"%n.id
                for variable in "grama","expresion","lectura":
                    #print "Cargando %s con el valor %s"%(variable,getattr(n,variable))
                    nota = limpiar_nota(getattr(n,variable))
                    baremo = limpiar_nota(getattr(n,"%s_baremo"%variable))
                    if nota != "NP" and baremo != 0:
                        nota_final = 100*int(nota)/int(baremo)
                    print "Tenemos la nota final",nota_final
                    notas.update({variable: nota_final})
            else:
                #print "No hay nota :("
                for variable in "grama","expresion","lectura":
                    #print "Cargando %s con el valor %s"%(variable,"-")
                    notas.update({variable: "-"})
            #print notas
            notas_trimestres.update({trimestre: notas})

        #print notas_trimestres
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
##        banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
##        img=Image(banner)
##        story.append(img)
        story.append(Spacer(0,40))
        ##Aquí un estilo adecuado, alineado derecha, para ventanilla, etc
        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=right>%s %s %s</para>"%(asistencia.alumno.nombre,asistencia.alumno.apellido1,asistencia.alumno.apellido2)
        story.append(Paragraph(cadena, estilo))
        cadena = "<para alignment=right>%s</para>"%(asistencia.alumno.direccion)
        story.append(Paragraph(cadena, estilo))
        cadena = "<para alignment=right>%s %s</para>"%(asistencia.alumno.cp,asistencia.alumno.ciudad)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,40))
        ##Intro
        cadena = "<para alignment=center><b>BOLETIN DE EVALUACION TRIMESTRAL</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        ##Datos del docu: alumno, grupo, profes
        cadena = "Nombre del alumno: <b>%s %s %s</b>"%(asistencia.alumno.nombre,asistencia.alumno.apellido1,asistencia.alumno.apellido2)
        story.append(Paragraph(cadena, estilo))
        cadena = "Grupo: <b>%s</b>"%asistencia.grupo.nombre
        story.append(Paragraph(cadena, estilo))
        profes = ""
        for c in asistencia.grupo.clases:
            profes = profes + "%s %s - "%(c.profesor.nombre,c.profesor.apellido1)
        cadena = "Profesores %s"%profes
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Faltas de asistencia
        ##calculamos todas las del trimestre haciendo un select en función del trimestre que sea
        if trimestre_imprimir == 1:
            debug("Mirando faltas del primer trimestre de %s"%asistencia.id)
            faltas_query = Falta.select(AND(Falta.q.asistenciaID==asistencia.id,OR(Falta.q.mes==9,Falta.q.mes==10,Falta.q.mes==11,Falta.q.mes==12)))
        elif trimestre_imprimir == 2:
            print "Mirando faltas del segundo trimestre"
            faltas_query = Falta.select(AND(Falta.q.asistenciaID==asistencia.id,OR(Falta.q.mes==1,Falta.q.mes==2,Falta.q.mes==3)))
        elif trimestre_imprimir == 3:
            print "Mirando faltas del tercer trimestre"
            faltas_query = Falta.select(AND(Falta.q.asistenciaID==asistencia.id,OR(Falta.q.mes==4,Falta.q.mes==5,Falta.q.mes==6)))
        else:
            print "a por todas las faltas"
            faltas_query = Falta.select(Falta.q.asistenciaID==asistencia.id)
        #...y pidiendo que nos sume las faltas
        faltas = faltas_query.sum('faltas')
        justificadas = faltas_query.sum('justificadas')
        cadena="Faltas de asistencia totales: %s   --  Faltas Justificadas:%s"%(faltas,justificadas)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Tabla con las notas
        tabla =[['EVALUACION','Primer Trimestre','Segundo Trimestre','Tercer Trimestre']]
        tabla.append(["GRAMMAR",\
            "%s"%(notas_trimestres[1]['grama']),\
            "%s"%(notas_trimestres[2]['grama']),\
            "%s"%(notas_trimestres[3]['grama'])])
        
        if (not asistencia.grupo.menores):
            tabla.append(["ORAL",\
                "%s"%(notas_trimestres[1]['expresion']),\
                "%s"%(notas_trimestres[2]['expresion']),\
                "%s"%(notas_trimestres[3]['expresion'])])
            tabla.append(["READING",\
                "%s"%(notas_trimestres[1]['lectura']),\
                "%s"%(notas_trimestres[2]['lectura']),\
                "%s"%(notas_trimestres[3]['lectura'])])
        
        t_notas = Table(tabla)
        print "Damos estilo ala tabla"
        t_notas.setStyle([('FONTNAME', (0,0), (-1,0), 'Times-Bold'),('FONTNAME', (0,0), (0,-1), 'Times-Bold')])
        #t_notas.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        story.append(t_notas)
        story.append(Spacer(0,85))
        ###Explicaciones y baremos
        #cadena="Comportamiento: M = Malo, R = Regular, B = Bueno, E = Muy Bueno"
        #story.append(Paragraph(cadena, estilo))
        #cadena="Realización tareas: N = Nunca, P = Pocas veces, A = A veces, C = Casi siempre, S = Siempre"
        #story.append(Paragraph(cadena, estilo))
        cadena="Las notas se calculan sobre 100. Para que un examen se considere aprobado se deberá superar el %d %%"%asistencia.grupo.curso.nota_aprobado
        story.append(Paragraph(cadena, estilo))
        cadena="NP: No Presentado"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        #~ ##Observaciones
        #~ cadena="<b>Observaciones del profesorado:                                          </b>"
        #~ story.append(Paragraph(cadena, estilo))
        #~ story.append(Spacer(0,80))
        if (asistencia.grupo.menores):
            ##Fecha y firmas
            cadena="Sello bueno del centro                    <para alignment=right>Firma de los padres</para>"
            story.append(Paragraph(cadena, estilo))
            story.append(Spacer(0,30))

        ##Pie de página

        #cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        return
    pass # End of class
