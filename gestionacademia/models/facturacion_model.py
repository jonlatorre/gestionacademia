# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

# Standard library imports
import logging

# Third party imports
from gestionacademia.utils import _importer
from gtkmvc import Model
import os
# Local library imports
from gestionacademia.utils import _config
from gestionacademia.models.preferences_model import PreferencesModel
from banco_model import BancoModel
from gestionacademia.utils._global import *

#Para generación de PDF
from gestionacademia.utils._imprimir import *

class FacturacionModel (Model):

    """El modelo que se encarga de genrar la facturacion y el fichero csb19 para
    la domiciliacion de los recibos.
    """
    BancoModel = BancoModel()
    preferences = None
    lista_cobros = []
    nif = ""
    sufijo = "000"
    ##Para el concepto
    ano_confeccion = ""
    mes_confeccion = ""
    dia_confeccion = ""
    ##Cuando hacemos el cargo
    ano_cargo = ""
    mes_cargo = ""
    dia_cargo = ""
    fecha_confeccion = "010111"
    fecha_cargo = "010111"
    concepto = ""
    nombre = ""
    banco = "0000"
    oficina = "0000"
    dc = "00"
    cuenta = "0000000000"
    procedimiento = "01"
    contenido = ""
    codigo_referencia = '0'*11+'1'
    importe_recibos = 0
    numero_recibos = 0
    importe_metalico = 0
    numero_metalico = 0
    importe_facturas = 0
    numero_facturas = 0
    def __init__(self):
        Model.__init__(self)
        self.preferences = PreferencesModel()
        ##Cargamos los datos de las preferencias
        self.nombre = self.normalizar(self.preferences.razon,40)
        for variable in ['banco','oficina','dc','cuenta']:
            setattr(self,variable,getattr(self.preferences,variable))
    def listado_bancos(self):
        """Generamos el PDF con todos los cobros por recibo"""
        fichero=os.path.join(get_print_path("Cobros"),'listado_cobros_recibo.pdf')
        story = []
        estiloHoja = getSampleStyleSheet()
        cabecera = estiloHoja['Heading4']
        cabecera.pageBreakBefore=0
        cabecera.keepWithNext=0
        ##cabecera.backColor=colors.cyan
        parrafo = Paragraph("Resumen de la Facturación del día %s/%s/%s"%(self.dia_cargo,self.mes_cargo,self.ano_cargo),cabecera)
        story.append(parrafo)
        story.append(Spacer(0,20))
        ##Tenemos la tabla de cargos y la tabla de resumen de bancos
        tabla =[['Banco','Apellidos, Nombre','Cuenta','Importe']]
        tabla_bancos =[['Banco','Recibos','Importe']]
        banco = 0
        nombre_banco=""
        total_banco = 0
        recibos_banco = 0
        texto_banco = ""
        total_todos_bancos = 0
        total_recibos_banco = 0
        ##Reordenamos la lista de cargos, primero por el código de banco...
        self.lista_cobros = sorted(self.lista_cobros,key=lambda cobro: cobro[2][3])
        ##...luego por el número de cuenta
        self.lista_cobros = sorted(self.lista_cobros,key=lambda cobro: cobro[2][0])
        ## Ahora recorremos la lista de cobros y preparamos las tablas
        for pago in self.lista_cobros:
            ##Cargamos el banco nuevo y el importe
            nuevo_banco = pago[2][0]
            importe = pago[3]
            ccc = pago[2]
            ##Comprobamos si aun no hemos cambiado de banco
            if nuevo_banco == banco:
                ##Sumamos el importe al total de este banco y el numero de cargos en el banco
                try:
                    total_banco = float(total_banco) + float(importe)
                except:
                    print "nO HEMOS PODIDO SUMAR sS AL BANCO %s"
                    print pago
                recibos_banco += 1
                tabla.append(['',pago[1],"%s-%s-%s-%s"%(ajustar(ccc[0],4),ajustar(ccc[1],4),ajustar(ccc[2],2),ajustar(ccc[3],10)),importe])
            else:
                ##Primero añadimos a la tabla del resumen de bancos los datos
                if not nuevo_banco == 0:
                    tabla_bancos.append(["%s[%s]"%(nombre_banco,banco),recibos_banco,total_banco])
                else:
                    ##es el primer banco o no tiene banco
                    pass
                    ##logging.debug(pago)
                    logging.debug("Tiene el banco a 0 no debería estar aquí")

                ##Sumamos los totales del banco al total final
                total_recibos_banco += recibos_banco
                total_todos_bancos += total_banco
                ##Ahora cargamos los nuevos datos
                banco=nuevo_banco
                self.BancoModel.buscar(banco)
                nombre_banco = self.BancoModel.nombre
                total_banco=float(importe)
                recibos_banco = 1
                ##Añadimos a la tabla la entrada del nuevo banco
                tabla.append(["%s(%s)"%(nombre_banco,banco),pago[1],"%s-%s-%s-%s"%(ajustar(ccc[0],4),ajustar(ccc[1],4),ajustar(ccc[2],2),ajustar(ccc[3],10)),importe])
        ##Añadimos el último banco, ya que sino se queda fuera
        total_recibos_banco += recibos_banco
        total_todos_bancos += total_banco
        tabla_bancos.append(["%s[%s]"%(nombre_banco,banco),recibos_banco,total_banco])
        ##Añadimos el total al resumen de bancos
        tabla_bancos.append(["Total:",total_recibos_banco,total_todos_bancos])
        t=Table(tabla_bancos)
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),
            ('LINEBEFORE', (0,0), (0,-1), 2, colors.black),
            ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
            ('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),
            ('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('ALIGN', (2,2), (-1,-1), 'RIGHT')])
        story.append(t)
        story.append(PageBreak())
        story.append(Spacer(0,20))
        cadena = "Listado de alumnos por bancos"
        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)
        story.append(Spacer(0,20))
        t = Table(tabla)
        t.setStyle([('LINEABOVE', (0,0), (-1,0), 2, colors.black),
            ('LINEBEFORE', (0,0), (0,-1), 2, colors.black),
            ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
            ('LINEAFTER', (0,0), (-1,-1), 0.25, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 2, colors.black),
            ('LINEAFTER', (-1,0), (-1,-1), 2, colors.black),
            ('ALIGN', (2,1), (2,-1), 'RIGHT')])
        story.append(t)
        doc=SimpleDocTemplate(fichero,pagesize=A4)
        #doc.build(story)
        doc.build(story, canvasmaker=NumberedCanvas)
        send_to_printer(fichero)
        return "En recibos tenemos %s cargos con un importe de %s \n"%(self.numero_recibos,self.importe_recibos)

    def listado_metalico(self,lista):
        fichero=os.path.join(get_print_path("Cobros"),'listado_cobros_metalico.pdf')
        texto = self.listado(lista,"que pagan en metalico",fichero)
        return "En metalico tenemos %s \n"%texto
    def listado_facturar(self,lista):
        fichero=os.path.join(get_print_path("Cobros"),'listado_cobros_factura.pdf')
        texto = self.listado(lista,"que necesitan factura",fichero)
        return "En factura tenemos %s \n"%texto
    def listado(self,lista,asunto,fichero):
        """Generamos un listado con los clientes que pagan en metalico o factura"""
        importe_listado = 0
        num_listado = 0
        estiloHoja = getSampleStyleSheet()
        story = []
##        cabecera = estiloHoja['Heading4']
##        cabecera.pageBreakBefore=0
##        cabecera.keepWithNext=0
##        cabecera.backColor=colors.cyan
##        parrafo = Paragraph("CABECERA DEL DOCUMENTO ",cabecera)
##        story.append(parrafo)
        cadena = " Listado de alumnos %s"%asunto
        estilo = estiloHoja['BodyText']
        parrafo2 = Paragraph(cadena, estilo)
        story.append(parrafo2)
        story.append(Spacer(0,20))

        tabla =[['Apellidos, Nombre','Importe']]
        for persona in lista:
            tabla.append([persona[0],persona[1]])
            importe_listado += float(persona[1])
            num_listado += 1
        story.append(Table(tabla))
        doc=SimpleDocTemplate(fichero,pagesize=A4,showBoundary=1)
        doc.build(story)
        send_to_printer(fichero)
        texto = "%s cargos con un importe de %s"%(num_listado,importe_listado)
        return texto

    def crear_fichero_19(self,fichero):
        #Ajustamos los campos...
        self.nif = self.ajustar(self.nif,9)
        self.sufijo = self.ajustar(self.sufijo,3)
        self.fechas()
        self.importe_recibos=0
        self.numero_recibos=0
        logging.debug( "Vamos a facturar el día %s en concepto de %s"%(self.fecha_cargo,self.fecha_confeccion) )
        #Vamos con la cabecera del presentador
        self.crear_presentador()
        #Vamos con la cabecera del ordenante
        self.crear_ordenante()
        # Ahora los cargos
        for cobro in self.lista_cobros:
            self.crear_individual(cobro)
        #Y para terminar los Totales
        self.crear_totales()
        
        logging.debug("Primero borramos el ficheros")
        try:
            os.unlink(fichero)
            logging.debug("Borrado")
        except Exception as e:
            #Es posible que no exista, asi que pasamo
            logging.debug("Problema al borrar")
            logging.debug(e)
            pass
        logging.debug("Abrimos el fichero")
        f = open(fichero,'w')
        logging.debug("Contenido creado, Escribiendo fichero %s"%fichero)
        f.write(self.contenido)
        f.close()
        #Vaciamos el buffer del fichero
        self.contenido = ""
        ##imprimimos las lista completa
        ##FIXME
        texto = "Se han creado %s recibos que suman un importe total de %s €"%(self.numero_recibos,self.importe_recibos)
        return texto

    def leer_fichero(self,fichero):
        """Funcion que lee un fichero CSB19 y nos muestra su contenido"""
        longitud_entrada = 164
        f = open(fichero,'r')
        datos = []
        entrada = f.read(longitud_entrada)
        while len(entrada):
            datos.append(entrada)
            entrada = f.read(longitud_entrada)
        f.close()
        datos.pop()
        ##Leemos la entrada del presentador (la primera)
        presentador = datos.pop(0)
        ##Leemos la entrada del presentador (la segunda, pero al borrar la del presentador ahora es la primera)
        ordenante = datos.pop(0)
        ##Leemos la entrada total general (la última)
        total_general = datos.pop()
        ##Leemos la entrada total ordenante (la última tras borrar a total general)
        total_ordenante = datos.pop()
        print "PRESENTADOR:"
        ##print presentador
        print "codigos","nif","sufijo","fecha","nombre","entidad","oficina"
        print presentador[0:4],presentador[4:13],presentador[13:16],presentador[16:22],presentador[22:28],presentador[28:68],presentador[88:92],presentador[92:96]
        print "ORDENANTE"
        ##print ordenante
        print "codigos","nif","sufijo","fecha","fecha cargo""nombre","cuenta","procedimiento"
        print ordenante[0:4],ordenante[4:13],ordenante[13:16],ordenante[16:22],ordenante[22:28],ordenante[28:68],ordenante[68:88],ordenante[96:98]
        ##Ahora solo quedan individuales
        print "CARGOS"
        print "Codigo.ref","\tTitular","\t\t\t\tcuenta","\t\t\timporte","concepto"
        for individual in datos:
            ##print individual
            print individual[16:28],individual[28:68],individual[68:88],individual[88:98],individual[114:154]
        print "TOTAL ORDENANTE"
        print "Suma importes","\tNumero de domici.","\tNumero de registros del ordenante"
        print total_ordenante[88:98],total_ordenante[104:114],total_ordenante[114:124]
        print "TOTAL GENERAL"
        print "N. Ordenates","Suma importes","\tNumero de domici.","\tNumero de registros del soporte"
        print total_general[68:72],total_general[88:98],total_general[104:114],total_general[114:124]


    # Non-public methods
    ##Funciones internas que crean los campos necesarios
    def crear_ordenante(self):
        """Funcion que crea el campo ordenante y lo añade al contenido"""
        cod_reg = "53"
        cod_dato = "80"
        relleno_e1= ' '*8
        relleno_e3= ' '*10
        relleno_f = ' '*40
        relleno_g = ' '*14
        cabecera_ordenante = cod_reg + cod_dato + self.nif + self.sufijo + self.fecha_confeccion + self.fecha_cargo + \
            self.nombre + self.ajustar(self.banco,4) + self.ajustar(self.oficina,4) + self.ajustar(self.dc,2) + self.ajustar(self.cuenta,8) + relleno_e1 + self.procedimiento + relleno_e3 + relleno_f + relleno_g + '\r\n'
        self.contenido += cabecera_ordenante
        logging.debug("Añadido el ordenante")
    def crear_presentador(self):
        """Funcion que crea el campo presentador y lo añade al contenido"""
        cod_reg = "51"
        cod_dato = "80"
        relleno_b3 = ' '*6
        relleno_d = ' '*20
        relleno_e3 = ' '*12
        relleno_f = ' '*40
        relleno_g = ' '*14
        cabecera_presentador = cod_reg + cod_dato + self.nif + self.sufijo + self.fecha_confeccion + \
            relleno_b3 + self.nombre + relleno_d + self.banco + self.oficina + relleno_e3 + relleno_f + relleno_g + '\r\n'
        self.contenido += cabecera_presentador
        logging.debug("Añadido el presentador")
    def crear_individual(self,cobro):
        ##Recibimos los datos de cada cobro, id, nombre, CCC, importe y concepto
        id = cobro[0]
        nombre=cobro[1]
        ccc=cobro[2]
        importe=cobro[3]
        concepto=cobro[4]
        #Sumamos el importe al total
        try:
            self.importe_recibos += float(importe)
        except:
            print "NO hemos podido genrerar el import para %s %s"%(nombre,importe)
        self.numero_recibos += 1
        cod_reg = "56"
        cod_dato = "80"
        #relleno de 16
        relleno_f = ' '*16
        #relleno de 8
        relleno_h = ' '*8
        ##Normalizamos (rellenamos) los campos nombre, importe y concepto
        nombre = self.normalizar(nombre,40)
        concepto = self.normalizar(concepto,40)

        #Vamos con el importe
        importe = self.ajustar(importe,10,2)

        individual = cod_reg + cod_dato + self.nif + self.sufijo + self.ajustar(id,12) + nombre + \
            self.ajustar(str(ccc[0]),4) + self.ajustar(str(ccc[1]),4) + self.ajustar(str(ccc[2]),2) + \
            self.ajustar(str(ccc[3]),10) + importe + relleno_f + concepto + \
            relleno_h + '\r\n'
        self.contenido += individual
        pass

    def crear_total_ordenante(self):
        cod_reg  = "58"
        cod_dato = "80"
        relleno_b2 = " "*12
        relleno_c  = " "*40
        relleno_d  = " "*20
        relleno_e2 = " "*6
        relleno_f3 = " "*20
        relleno_g  = " "*18
        ##FIXME ajustar el formato del importe total
        importe_recibos = str(self.importe_recibos)
        logging.debug("ORDENANTE: Tenemos %i pagos que suman %s"%(len(self.lista_cobros),importe_recibos))
        total_ordenante = cod_reg + cod_dato + self.nif + self.sufijo + relleno_b2 \
            + relleno_c + relleno_d + self.ajustar(importe_recibos,10,2) + relleno_e2 \
            + self.ajustar(len(self.lista_cobros),10) + self.ajustar(len(self.lista_cobros)+2,10) + relleno_f3 \
            + relleno_g + '\r\n'
        self.contenido += total_ordenante
        pass
    def crear_total_general(self):
        cod_reg  = "59"
        cod_dato = "80"
        relleno_b2 = " "*12
        relleno_c  = " "*40
        relleno_d2  = " "*16
        relleno_e2 = " "*6
        relleno_f3 = " "*20
        relleno_g  = " "*18
        num_ordenantes = "0001"
        ##FIXME ajustar el formato del importe total
        importe_recibos = str(self.importe_recibos)
        logging.debug("GENERAL: Tenemos %i pagos que suman %s"%(len(self.lista_cobros),importe_recibos))
        total_general = cod_reg + cod_dato + self.nif + self.sufijo + relleno_b2 +\
            relleno_c + num_ordenantes + relleno_d2 + self.ajustar(importe_recibos,10,2) + relleno_e2 + \
            self.ajustar(len(self.lista_cobros),10) + self.ajustar(len(self.lista_cobros)+4,10) + relleno_f3 + relleno_g  + '\r\n'
        self.contenido += total_general
        pass
    def crear_totales(self):
        """creamos los totales"""
        self.crear_total_ordenante()
        self.crear_total_general()
        pass
    def normalizar(self,campo,longitud):
        """Fucnion que normaliza el campo: Lo pasa a mayusculas, lo recorta
            a longitud si hace falta o lo rellena con espacios hasta la longitud"""
        campo = str(campo)
        campo = campo.upper()
        if len(campo)>longitud:
            #recortamos hasta longitud
            campo = campo[0:longitud]
        if len(campo)<longitud:
            #rellenamos hasta lamgitud
            campo += ' '*(longitud-len(campo))
        return campo
    def ajustar(self,numero,longitud, num_decimales=0):
        """Función que ajusta a la derecha el numero añadiendo por la izquierda los "0" que sean necesario"""
        unidades = str(numero).split('.')[0]
        if num_decimales == 0:
            numero = unidades
        else:
            try:
                decimales = str(numero).split('.')[1]
                decimales = decimales[0:num_decimales]
                decimales = decimales + '0'*(num_decimales-len(decimales))
            except:
                ##print "Añadimos %s 0 como decimales"%num_decimales
                decimales = '0'*num_decimales
            numero = unidades + str(decimales[0:num_decimales])

        if len(numero)<longitud:
##            print "Hacen falta ceros a la izquierda..."
            numero = '0'*(longitud-len(numero))+numero
        return numero
    def fechas(self):
        ##Ajustamos la fechas
        ##Pasamos todo a str...
        ano_cargo      = str(self.ano_cargo)
        mes_cargo      = str(self.mes_cargo)
        dia_cargo      = str(self.dia_cargo)
        ano_confeccion = str(self.ano_confeccion)
        mes_confeccion = str(self.mes_confeccion)
        dia_confeccion = str(self.dia_confeccion)
        ##los años son solo 2 dígitos
        if len(ano_cargo)==4:
            ano_cargo=ano_cargo[-2:]
        if len(ano_confeccion)==4:
            ano_confeccion=ano_confeccion[-2:]
        ##os días y meses tiene que tener 2 dígitos
        if len(dia_cargo)==1:
            dia_cargo="0"+dia_cargo
        if len(dia_confeccion)==1:
            dia_confeccion="0"+dia_confeccion
        if len(mes_cargo)==1:
            mes_cargo="0"+mes_cargo
        if len(mes_confeccion)==1:
            mes_confeccion="0"+mes_confeccion
        ##Pasamos las fechas ajustadas
        self.fecha_confeccion = dia_confeccion + mes_confeccion + ano_confeccion
        self.fecha_cargo= dia_cargo + mes_cargo + ano_confeccion
    # Observed properties

    pass # end of class
