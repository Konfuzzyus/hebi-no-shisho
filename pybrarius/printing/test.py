# -*- coding: utf-8 -*-
"""
    Pybrarius - A small scale pythonic library management tool
    Copyright (C) 2013 - 2014 Christian Meyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__='''$Id$'''
import reportlab.pdfgen.canvas
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128, code39, code93, eanbc
from reportlab.graphics.shapes import Drawing

def run():
    c = reportlab.pdfgen.canvas.Canvas('barcodetest.pdf', pagesize=pagesizes.A4)

    framePage(c, 'Hebi-No-Shisho Barcode Test Page' )
    
    y = 700
    yd = 50
    xb = 40
    xs = 240

    y = y-yd
    mybarcode = code39.Standard39(barWidth=inch * 0.010, value="CD3910", checksum=0)
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard39 10 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code39.Standard39(barWidth=inch * 0.015, value="CD3915", checksum=0)
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard39 15 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code39.Standard39(barWidth=inch * 0.020, value="CD3930", checksum=0)
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard39 20 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code93.Standard93(barWidth=inch * 0.010, value="CD9310")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard93 10 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code93.Standard93(barWidth=inch * 0.015, value="CD9315")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard93 15 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code93.Standard93(barWidth=inch * 0.020, value="CD9320")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard93 20 mil' % mybarcode.encoded)
    
    y = y-yd
    mybarcode = code128.Code128(barWidth=inch * 0.010, value="C12810")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard128 10 mil' % mybarcode.value)
    
    y = y-yd
    mybarcode = code128.Code128(barWidth=inch * 0.015, value="C12815")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard128 15 mil' % mybarcode.value)
    
    y = y-yd
    mybarcode = code128.Code128(barWidth=inch * 0.020, value="C12820")
    mybarcode.drawOn(c, xb, y)
    c.drawString(xs, y, '%s - Standard128 20 mil' % mybarcode.value)
    
    y = y-yd-10
    mydrawing = Drawing()
    mybarcode = eanbc.Ean13BarcodeWidget(barHeight=inch * 0.5, barWidth=inch * 0.015, value="123456789012")
    mydrawing.add(mybarcode)
    mydrawing.drawOn(c, xb, y)
    c.drawString(xs, y, 'EAN13')
    
    c.save()

def framePage(canvas, title):
    canvas.setFont('Times-BoldItalic',20)
    canvas.drawString(inch, 10.5 * inch, title)

    canvas.setFont('Times-Roman',10)
    canvas.drawCentredString(4.135 * inch, 0.75 * inch,
                            'Page %d' % canvas.getPageNumber())

    #reset carefully afterwards
    canvas.setLineWidth(1)
    canvas.setStrokeColorRGB(0,0,0)

if __name__ == '__main__':
    run()

