# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE


# Standard library imports
import os.path

# Third party library imports
from gtkmvc import Model
from gtkmvc.model import SQLObjectModel
from gtk import ListStore

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject

from datetime import date

import new
import re

#Para trabajar con calendarios
from calendar import Calendar

# Local library imports
from database_model import Grupo, Clase, Asistencia, Curso, Profesor, Alumno, Festivo, Nota
from gestionacademia.models.nota_model import NotaModel
from gestionacademia.utils import _config
#Para generación de PDF
from gestionacademia.utils._imprimir import *
from gestionacademia.utils._global import *


class GrupoModel (Model):

    """An almost empty model for the 'About' dialog. It has been added
    to show how models might be used to separate the logic. In the
    spirit of this tutorial, the usage of an observable property for
    the credits text is an exaggeration.
    Metodos públicos:
    set_alumno
    guardar
    """
    g = None
    num_max = 0
    menores = False
    ##Esta es la lista de grupos
    lista = ListStore(int, str, str,int,int,str,str,str)
    ##Para almacenar las lista de alumnos en un listore (id, nombre, apellidos y DNI)
    lista_alumnos = ListStore(int, int, str, str, str, str, str)
    combo_alumnos = ListStore(int, str)
    ##La lista de clases de un grupo concreto
    lista_clases = ListStore(int,str,str,str,str)

    def __init__(self):

        """Constructor for GrupoModel initialises the model with its parent
        class, then sets credits to the contents of a file.

        """
        Model.__init__(self)
        self.lista_alumnos.clear()
        self.rellenar_lista()


    def rellenar_lista(self):
        self.lista.clear()
        for grupo in Grupo.select(orderBy=Grupo.q.nombre):
            ##Primero sacamos la lista de alumnos para calcular los confirmados, sin confirmar y edades...
            confirmados=0
            sinconfirmar=0
            maxi = ""
            mini = ""
            fechas=[]
            lista = grupo.alumnos
            for asistencia in lista:
                if asistencia.confirmado:
                    confirmados+=1
                else:
                    sinconfirmar+=1
                fechas.append(asistencia.alumno.fecha_nacimiento)
            ##Ahora sacamos las clases para mostrar horario
            horario=""
            for clase in grupo.clases:
                horario=horario+"%s : %s "%(clase.dia_semana,clase.horario)
            ##self.lista.append([grupo.id,grupo.nombre,grupo.curso.nombre,confirmados,sinconfirmar,min(fechas),max(fechas),horario])
            try:
                if grupo.curso == None:
                    curso = "Sin curso definido"
                else:
                    curso = str(grupo.curso.nombre)
            except:
                curso = "Sin curso definido"
            try:
                maxi = max(fechas).year
            except:
                maxi = ""
            try:
                mini = min(fechas).year
            except:
                mini = ""
            #print grupo.id,grupo.nombre,curso,int(confirmados),int(sinconfirmar),str(maxi),str(mini),str(horario)
            self.lista.append([grupo.id,grupo.nombre,curso,int(confirmados),int(sinconfirmar),str(maxi),str(mini),str(horario)])

        return

    def rellenar_lista_alumnos(self):
        debug("refrescando la lista de alumnos al cargar nuevo grupo")
        self.lista_alumnos.clear()
        self.combo_alumnos.clear()
        lista = Grupo.get(self.id).alumnos
        for asistencia in lista:
            alumno = asistencia.alumno
            self.lista_alumnos.append([asistencia.id,alumno.id,alumno.nombre,"%s %s"%(alumno.apellido1,alumno.apellido2),alumno.dni,str(alumno.fecha_nacimiento),str(asistencia.confirmado)])
            ##Rellenamos el listado para el combo
            self.combo_alumnos.append([asistencia.id,"%s - %s %s, %s"%(alumno.id,alumno.apellido1,alumno.apellido2,alumno.nombre)])
    def rellenar_lista_clases(self):
        self.lista_clases.clear()
        lista = Grupo.get(self.id).clases
        for clase in lista:
            if clase.aula:
                aula = "%s - %s"%(clase.aula.piso,clase.aula.numero)
            else:
                aula = "Sin aula definida"
            if clase.profesor:
                profesor_apellido1 = clase.profesor.apellido1
                profesor_nombre = clase.profesor.nombre
            else:
                profesor_apellido1 = "sin_datos"
                profesor_nombre = "Sin profesor"

            self.lista_clases.append([clase.id,clase.dia_semana,aula,"%s,%s"%(profesor_apellido1,profesor_nombre),clase.horario])

    def cargar(self,id):
        self.lista_alumnos.clear()
        self.lista_clases.clear()

        if id == -1:
            debug("Es un grupo nuevo?")
            self.id=-1
            self.nombre=""
            self.cursoID=0
            self.num_max=14
            self.menores = False
        else:
            self.g = Grupo.get(id)
            self.id = self.g.id
            self.nombre = self.g.nombre
            if not self.g.cursoID == None:
                self.cursoID = self.g.cursoID
            else:
                self.cursoID = -1
            self.menores = self.g.menores
            self.num_max = self.g.num_max
            self.rellenar_lista_alumnos()
            self.rellenar_lista_clases()

    def guardar(self):
        if self.id==-1:
            ##FIXME estoy puede fallar, al añadir alumnos y clases a un grupo que AUN no existe
            debug("Creando el grupo")
            self.g = Grupo(nombre = self.nombre,curso=Curso.get(self.cursoID),num_max=self.num_max,menores = self.menores)
            self.id = self.g.id
        else:
            self.g.nombre = self.nombre
            self.g.curso = Curso.get(self.cursoID)
            self.g.num_max = self.num_max
            self.g.menores = self.menores
        ##Antes de salir refrescamos la lista
        self.rellenar_lista()
        return

    ##Funciones para añadir y quitar alumnos del grupo
    def quitar_alumno(self,id):
        asis = Asistencia.get(id)
        debug("vamos a quitar el alumnos %s del grupo"%asis.alumno.id)
        asis.destroySelf()
        self.rellenar_lista_alumnos()
    def anadir_alumno(self,id):
        if self.id == -1:
            print "Antes debemos guardar el grupo, ya que no existe"
            self.guardar()
        ##Primero comprobamos si el alumno ya está en la lista
        for asistencia in self.g.alumnos:
            if asistencia.alumnoID == id:
                print "El alumno ya está en la lista!"
                return
        ##Obtenemos el alumno de la id
        a = Alumno.get(id)
        print "Añadiendo a %s %s %s"%(a.nombre,a.apellido1,a.apellido2)
        ##Creamos una asistencia sin confirmar para ese alumno
        c = Asistencia(grupo=self.g,alumno=a,confirmado=False)
        ##Refrescamos la lista
        self.rellenar_lista_alumnos()
    def anadir_clase(self,clase):
        print "añadimos la clase %s"%clase.id
        if self.id == -1:
            print "Antes debemos guardar el grupo, ya que no existe"
            self.guardar()
        self.g.addClase(clase)
        self.rellenar_lista_clases()
        return
    def quitar_clase(self,id):
        #clase = Clase.get(id)
        print "quitando la clase %s"%id
        Clase.delete(id)
        self.rellenar_lista_clases()
        return
    def imprimir_lista(self):
        """Sacamos un PDF con el listado completo de grupos"""
        print "Imprimiendo listado completo de grupos"
        num = 0
        fichero = get_print_path('Grupos')+"/Listado_completo.pdf"
        estiloHoja = getSampleStyleSheet()
        story = []
##        ##Vamos con la cabecera
##        banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
##        img=Image(banner)
##        story.append(img)
        ##Intro
        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=center><b>LISTADO DE GRUPOS</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        tabla=[['ID','Nombre','Curso','Cuota','Conf.','SinConf','Fecha Min','Fecha Max','Horario']]
        for grupo in Grupo.select(orderBy=Grupo.q.nombre):
            num += 1
            ##Primero sacamos la lista de alumnos para calcular los confirmados, sin confirmar y edades...
            confirmados=0
            sinconfirmar=0
            fechas=[]
            lista = grupo.alumnos
            for asistencia in lista:
                if asistencia.confirmado:
                    confirmados+=1
                else:
                    sinconfirmar+=1
                fechas.append(asistencia.alumno.fecha_nacimiento)
            ##Ahora sacamos las clases para mostrar horario
            horario=""
            for clase in grupo.clases:
                horario=horario+"%s : %s "%(clase.dia_semana,clase.horario)
            ##self.lista.append([grupo.id,grupo.nombre,grupo.curso.nombre,confirmados,sinconfirmar,min(fechas),max(fechas),horario])
            ##Intentamos calcular el año máximo y el minimo
            try:
                maxi = max(fechas).year
            except:
                maxi = ""
            try:
                mini = min(fechas).year
            except:
                mini = ""
            tabla.append([grupo.id,grupo.nombre,grupo.curso.nombre,grupo.curso.precio,confirmados,sinconfirmar,mini,maxi,horario])

        t = Table(tabla)
        t.setStyle([('FONTSIZE',(0,0),(-1,-1),8),('FONTSIZE',(-1,0),(-1,-1),6),('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green)])
        story.append(t)
        story.append(Spacer(0,20))

        story.append(Spacer(0,240))

##        ##Pie de página
##        cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
##        story.append(Paragraph(cadena, estilo))
##        cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
##        story.append(Paragraph(cadena, estilo))
##        story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=landscape(A4),showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        ##Fin imprimir_lista
        return num
    def todas_planillas_asistencia(self,mes):
        print "Imprimiendo las planillas del mes %s"%mes
        num = 0
        ano = date.today().year
        #FIXME esto estaría mejor en el controlador o en la vista
        if mes == 1:
            print "Estamos trabajando cone l mes de enero!"
            res = pedir_confirmacion("Hemos detectado que quieres imprimir las notas de Enero, ¿quieres que sea el mes de Enero de %s ?"%(ano+1),"¿Usar el año que viene?")
            if res:
                ano = ano + 1;
        for g in Grupo.select(orderBy=Grupo.q.nombre):
            print "Imprimiendo planilla asistencia del grupo %s"%g.id
            self.cargar(g.id)
            try:
                self.imprimir_planilla_asistencia(ano,mes)
                num +=1
            except:
                print "Fallo imprimiendo la planilla de asistencia del grupo %s el mes %s/%s"%(self.id,mes,ano)

        return num
    def todas_planillas_notas(self,mes):
        num = 0
        for g in Grupo.select(orderBy=Grupo.q.nombre):
            self.cargar(g.id)
            self.imprimir_planilla_notas(mes)
            num += 1
        return num
    def imprimir_planilla_notas(self,trimestre):
        ##Para la impresion de la planilla de notas
        fichero = get_print_path("Grupos")+"/Ficha_Notas_Trimestre%s_Grupo%s.pdf"%(trimestre,self.g.id)
        estiloHoja = getSampleStyleSheet()
        story = []
        ##Vamos con la cabecera
        ##banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
        ##img=Image(banner)
        ##story.append(img)
        story.append(Spacer(0,40))
        ##Intro
        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=center><b>RELACION DE ALUMNOS POR GRUPO PARA CALIFICACIONES</b></para>"
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,10))
        ##Datos del docu: alumno, grupo, profes
        cadena = "Grupo: <b>%s %s</b>"%(self.g.id,self.g.nombre)
        cadena = cadena + "     Curso: <b>%s</b>"%self.g.curso.nombre
        story.append(Paragraph(cadena, estilo))
        profes = ""
        for c in self.g.clases:
            profes = profes + "; %s %s, %s "%(c.profesor.nombre,c.profesor.apellido1,c.profesor.apellido2)
        cadena = "Profesores %s"%profes
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))

        ##Tabla con las notas (diferente para peques y adultos
        if re.search("junior",str(self.g.curso.nombre).lower()) or re.search("begin",str(self.g.curso.nombre).lower()):
            ##Solo para los peques
            tabla =[['Num.','Apellidos, Nombre','Control1','Control2','Control Final','Compor.','Tareas']]
            for asis in self.g.alumnos:
                a = asis.alumno
                tabla.append([a.id,"%s %s,%s"%(a.apellido1,a.apellido2,a.nombre),"   /   ","   /   ","   /   ","  ","  "])
            t = Table(tabla)
            t.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green),('FONTSIZE',(0,0),(-1,-1),9)])
            story.append(t)
            story.append(Spacer(0,20))
        else:
            ##Adultos llevan todos los conceptos
            tabla =[['Num.','Apellidos, Nombre','Ctrl1','Ctrl2','Ctrl Final','Compor.','Tareas','Gramá.','Expre.','Lectura']]
            for asis in self.g.alumnos:
                a = asis.alumno
                tabla.append([a.id,"%s %s,%s"%(a.apellido1,a.apellido2,a.nombre),"   /   ","   /   ","   /   ","  ","  ","   /   ","   /   ","   /   "])
            t = Table(tabla)
            t.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue), ('TEXTCOLOR',(1,1), (2,-1),colors.green),
                ('FONTSIZE',(0,0),(-1,-1),10)])
            story.append(t)
            story.append(Spacer(0,20))

        ##Explicaciones y baremos
        cadena="Comportamiento: M = Malo, R = Regular, B = Bueno, E = Muy Bueno"
        story.append(Paragraph(cadena, estilo))
        cadena="Realización tareas: N = Nunca, P = Pocas veces, A = A veces, C = Casi siempre, S = Siempre"
        story.append(Paragraph(cadena, estilo))

        ##Pie de página

        #cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
        #story.append(Paragraph(cadena, estilo))
        #cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
        #story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=0)
        doc.build(story)
        send_to_printer(fichero)
        return
    def imprimir_planilla_asistencia(self,ano,mes):
        ##Para la impresion de la planilla de asistencia a clase
        logging.debug("Vamos a imprimir la planilla de asistencia del mes %s del año %s"%(mes,ano))
        fichero = get_print_path('Grupos')+"/Ficha_Asistencia_Mes%s_Grupo_%s.pdf"%(mes,self.g.id)
        calendario = Calendar(0)

        conversion = dict(lunes=0,martes=1,miercoles=2,jueves=3,viernes=4,sabado=5,domingo=6)
        iter_mes = calendario.itermonthdays2(ano,mes)
        ##Comprobamos si este mes es el inicio del curso
        try:
            res = Festivo.select(AND(Festivo.q.ano==ano,Festivo.q.mes==mes,Festivo.q.inicio==True))
            inicio = res[0].dia
            logging.debug("El inicio del curso es el %s",inicio)
        except:
            ##No es el inicio, ponemos a la variable inicio a 0 así el día siempre será mayor que 0
            inicio = 0
        ##Comprobamos si este mes es el inicio del curso
        try:
            res = Festivo.select(AND(Festivo.q.ano==ano,Festivo.q.mes==mes,Festivo.q.fin==True))
            fin = res[0].dia
            logging.debug("El fin de curso es el %s",fin)
        except:
            logging.debug("No es el fin")
            ##No es el fin, ponemos a la variable fin a 31 así el día siempre será menor que 31
            fin = 31

        estiloHoja = getSampleStyleSheet()
        story = []
##        ##Vamos con la cabecera
##        banner = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
##        img=Image(banner)
##        story.append(img)
        ##Intro
        estilo = estiloHoja['BodyText']
        cadena = "<para alignment=center><b>RELACION DE DIAS LECTIVOS DEL MES %s %s</b></para>"%(nombre_mes(mes),ano)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Datos del docu: alumno, grupo, profes
        cadena = "Grupo: <b>%s - %s</b>"%(self.g.id,self.g.nombre)
        story.append(Paragraph(cadena, estilo))
        cadena = "Curso: <b>%s</b>"%self.g.curso.nombre
        story.append(Paragraph(cadena, estilo))
        cadena = "Numero de alumnos: <b>%s</b>"%len(self.g.alumnos)
        story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Lista de libros
        for l in self.g.curso.libros:
            cadena = "Libro: %s - %s"%(l.titulo,l.autor)+" Editorial: %s "%(l.editorial)
            story.append(Paragraph(cadena, estilo))
            cadena = "      ISBN: %s"%(l.isbn)
            story.append(Paragraph(cadena, estilo))
        story.append(Spacer(0,20))
        ##Tabla con el horario
        tabla =[['Día','Horario','Aula','Profesor']]
        for c in self.g.clases:
            tabla.append([c.dia_semana,c.horario,"%s - %s"%(c.aula.numero,c.aula.piso),"%s %s"%(c.profesor.nombre,c.profesor.apellido1)])
        t = Table(tabla)
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),('LINEBEFORE', (0,0), (0,-1), 2, colors.black),
            ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT')])
        story.append(t)
        story.append(Spacer(0,20))

        ##Tabla con los días
        fila = ['Num.','F. Nac.','Apellidos, Nombre','Cnf.']
        dia_old = []
        for dia in iter_mes:
            if dia[0] == 0:
                continue
            for clase in self.g.clases:
                if conversion[limpiar_tildes(clase.dia_semana).lower()] == dia[1] :
                    ##Comprobamos si no es festivo
                    res = Festivo.select(AND(Festivo.q.ano==ano,Festivo.q.mes==mes,Festivo.q.dia==dia[0],Festivo.q.inicio==False,Festivo.q.fin==False))
                    if not len(list(res)):
                        ##Comrpobamos si ya hemos añadido ese día por tener 2h
                        ##FIXME
                        if dia == dia_old:
                            debug("Ya habiamos añadido este día!")
                        ##Sino comprobamos que el día sea después del inicio y antes del fin
                        elif ( dia[0] >= inicio and dia[0] <= fin ):
                            fila.append("%i"%(dia[0]))
                        else:
                            debug("El día %s esta antes o despues del inicio del curso!"%dia[0])
                    else:
                        debug("El día %s es festivo"%dia[0])
                    dia_old = dia
        longitud = len(fila)
        relleno = longitud - 3
        tabla =[fila]
        for asis in sorted(self.g.alumnos,key= lambda a: a.alumnoID):
            a = asis.alumno
            fila_alumno = [a.id,a.fecha_nacimiento,"%s %s, %s"%(a.apellido1,a.apellido2,a.nombre),asis.confirmado]
            while not len(fila_alumno)==longitud:
                fila_alumno.append("  ")
            tabla.append(fila_alumno)
        t = Table(tabla)
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),('LINEBEFORE', (0,0), (0,-1), 2, colors.black),
        ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),('FONTSIZE',(0,0),(-1,-1),8),('FONTSIZE',(2,0),(2,-1),9)])

        story.append(t)
        story.append(Spacer(0,20))

##        story.append(Spacer(0,240))

##        ##Pie de página
##        cadena="<para alignment=center><b>Genaro Oraá,6 - 48980 SANTURTZI (Spain)- Tlf. + 34 944 937 005 - FAX +34 944 615 723</b></para>"
##        story.append(Paragraph(cadena, estilo))
##        cadena="<para alignment=center><b><a href=\"http:\\www.eide.es\">www.eide.es</a> - e-mail: eide@eide.es</b></para>"
##        story.append(Paragraph(cadena, estilo))
##        story.append(Spacer(0,20))
        ##Sacamos el docu
        doc=SimpleDocTemplate(fichero,pagesize=A4)
        doc.build(story)
        send_to_printer(fichero)
        return
    def imprimir_notas(self,trimestre):
        """Funcion que imprime todas las notas de un grupo dado en un trimestre concreto"""
        print "trimeste",trimestre
        for asistencia in self.g.alumnos:
            try:
                nm = NotaModel()
                print "Mandamos imprimir las notas de la asistencia %i"%asistencia.id
                nm.imprimir_nota(asistencia,trimestre)
            except Exception,e:
                if e == "list index out of range":
                    print "No hay nota aun!"
                else:
                    print "Otro error:", e


    def borrar(self):
        print "Borramos el grupo ya cargado %s"%self.id
        for asis in self.g.alumnos:
            print "Borrando asistencia %s del alumnuno %s"%(asis.id,asis.alumno.id)
            for nota in asis.notas:
                Nota.delete(nota.id)
            Asistencia.delete(asis.id)
        for clase in self.g.clases:
            print "Borrando la clase %s"%clase.id
            Clase.delete(clase.id)
        Grupo.delete(self.id)
        self.rellenar_lista()
    pass # End of class
