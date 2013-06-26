# -*- coding: utf-8 -*-
### BEGIN LICENSE
# This file isls .. in the public domain
### END LICENSE

import os
import logging

from gestionacademia.utils import _config
from gestionacademia.utils._global import *

#Para generación de PDF
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4,A5,landscape
from reportlab.lib import colors
from reportlab.lib.units import cm,mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
##from PIL import Image

PAGE_HEIGHT=29.7*cm
PAGE_WIDTH=21*cm
capitulo = 'Cap %d' % 1
tema = 'Descripcion General del Edificio'
##logo = Image.open('./icons/logo.png')
logo = os.path.join(_config.get_data_path(), 'media', 'banner_eide.png')
##logo = 'el logo de 40x40pixels'
arquitecto = 'Nombre del arquitecto'
empresa = 'nombre de la empresa'
proyecto = 'Descripcion del proyecto'
situacion = 'poblacion, municipio'
referencia = 'referencia interna'

l1 = (1*cm, PAGE_HEIGHT-2.3*cm, PAGE_WIDTH-1.5*cm, PAGE_HEIGHT-2.3*cm)
l2 = (1*cm, 1.5*cm, PAGE_WIDTH-1.5*cm, 1.5*cm)
lineas = [l1,l2]

estiloencabezado = ParagraphStyle('',
                              fontName = 'DejaVuBd',
                              fontSize = 10,
                              alignment = 0,
                              spaceBefore = 0,
                              spaceAfter = 0,
                              leftIndent = -1*cm,
                              rightIndent = -0.7*cm)

estilonormal = ParagraphStyle('',
                              fontName = 'DejaVu',
                              fontSize = 10,
                              alignment = 4,
                              spaceBefore = 0,
                              spaceAfter = 0,
                              firstLineIndent = 1*cm,
                              topIndent =-1*cm,
                              leftIndent = -1*cm,
                              rightIndent = -0.7*cm)

#importar una fuente TT
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))
##pdfmetrics.registerFont(TTFont('DejaVuBd', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansBold.ttf'))
##pdfmetrics.registerFont(TTFont('DejaVuBdIt', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansBoldOblique.ttf'))
##pdfmetrics.registerFont(TTFont('DejaVuIt', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansOblique.ttf'))
##registerFontFamily('Dejavu', normal = 'DejaVu', bold = 'DejaVuBd', italic = 'DejaVuIt', boldItalic = 'DejaVuBdIt')
registerFontFamily('Dejavu', normal = 'DejaVu', bold = 'DejaVu', italic = 'DejaVu', boldItalic = 'DejaVu')


def get_print_path(modulo):
    """Devuelve el directorio donde se almacenan los PDF"""
    print_path = os.path.join(os.path.expanduser('~'),'Documentos',modulo)
    ##Si no existe el directorio lo creamos
    if not os.path.isdir(print_path):
        logging.debug("Creando el dir para %s"%modulo)
        os.mkdir(print_path)
    return print_path
def send_to_printer(fichero):
    #logging.debug("Vamos a mandar a la impresora %s"%fichero)
    logging.debug("No lo mandamos a la impresora %s"%fichero)
    #os.system("lpr %s"%fichero)
def myFirstPage(canvas, doc):
    canvas.saveState()

    ##    Lineas
    canvas.setStrokeColor('Grey')
    canvas.setLineWidth(0.01)
    canvas.lines(lineas)

    ##    Textos
    canvas.setFont('DejaVu',7)
    ##    Cabecera
    canvas.drawInlineImage(logo, 1*cm, PAGE_HEIGHT-2.*cm, width = 40, height = 40)
    canvas.drawString(2.5*cm, PAGE_HEIGHT-1.*cm, 'ARQUITECTO: ' + arquitecto)
    canvas.drawString(2.5*cm, PAGE_HEIGHT-1.5*cm, 'EMPRESA: ' + empresa)

    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-1.0*cm, capitulo)

    canvas.drawRightString(PAGE_WIDTH-1.7*cm, PAGE_HEIGHT-1*cm, 'PROYECTO: '+ proyecto)
    canvas.drawRightString(PAGE_WIDTH-1.7*cm, PAGE_HEIGHT-1.5*cm, 'SITUACION: ' + situacion)
    canvas.drawRightString(PAGE_WIDTH-1.7*cm, PAGE_HEIGHT-2.*cm, 'REFERENCIA: ' + referencia)
    ##    Pie

    canvas.drawCentredString(PAGE_WIDTH/2.0, 1.0 * cm, u'%s' % tema)
    canvas.drawRightString(PAGE_WIDTH - 1.7 * cm, 1.0 * cm, u'Pág. %d' % doc.page)

    canvas.restoreState()

## {{{ http://code.activestate.com/recipes/546511/ (r2)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._codes = []
    def showPage(self):
        self._codes.append({'code': self._code, 'stack': self._codeStack})
        self._startPage()
    def save(self):
        debug("Estamos guardando el docu y le vamos a añadir el indice de pag.")
        """add page info to each page (page x of y)"""
        # reset page counter
        self._pageNumber = 0
        for code in self._codes:
            # recall saved page
            self._code = code['code']
            self._codeStack = code['stack']
            self.setFont("Helvetica", 7)
            self.drawRightString(200*mm, 20*mm,
                "page %(this)i of %(total)i" % {
                   'this': self._pageNumber+1,
                   'total': len(self._codes),
                }
            )
            canvas.Canvas.showPage(self)
        self._doc.SaveToFile(self._filename, self)

    ## tenemos que llamar al build tal que así doc.build(elements, canvasmaker=NumberedCanvas)
## end of http://code.activestate.com/recipes/546511/ }}}

