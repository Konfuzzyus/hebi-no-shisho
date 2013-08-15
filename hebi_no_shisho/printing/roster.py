"""
    Hebi no Shisho - A small scale pythonic library management tool
    Copyright (C) 2013 Christian Meyer

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

from reportlab.lib import units, pagesizes
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab import platypus
from reportlab.lib import styles

left_margin = units.mm * 25
base_margin = units.mm * 15
pagesize = pagesizes.A4

bottom_line_y = base_margin
top_line_y = pagesize[1] - base_margin - units.mm * 5
sheet_height = top_line_y - bottom_line_y
sheet_width = pagesize[0] - left_margin - base_margin

sheet_margin = units.mm * 3
sheet_title_size = 14
sheet_user_area_height = sheet_height - 2*sheet_margin - sheet_title_size
user_rows = 15
user_columns = 2
user_height = sheet_user_area_height / user_rows
user_width = sheet_width / user_columns

class UserRoster():
    
    def __init__(self, userlist):
        self.userlist = userlist
        self.canvas = None
        
    def write_pdf(self, filename):
        self.canvas = canvas.Canvas(filename=filename,
                                 pagesize=pagesize)
        
        for form in sorted(self.userlist.get_forms(), key=lambda form: form.get_name()):
            self._setup_page()
            self._draw_sheet(form)
            self.canvas.showPage()
        
        self.canvas.save()
        self.canvas = None
    
    def _setup_page(self):
        self.canvas.saveState()
        self.canvas.translate(left_margin, 0)
        self.canvas.line(0, bottom_line_y, sheet_width, bottom_line_y)
        self.canvas.line(0, top_line_y, sheet_width, top_line_y)
        self.canvas.translate(0, top_line_y)
        self.canvas.setFont('Helvetica-Oblique', 8)
        self.canvas.drawString(0, 2, 'Hebi-no-Shisho User Roster')
        self.canvas.restoreState()
        
        self.canvas.translate(left_margin, base_margin)
    
    def _draw_sheet(self, form):
        self.canvas.setFont('Helvetica', sheet_title_size)
        self.canvas.drawString(0, sheet_height - sheet_title_size - sheet_margin, form.get_name())
        
        user_key = lambda user: user.name
        users = []
        users.extend(sorted(form.get_teachers(), key=user_key))
        users.extend(sorted(form.get_pupils(), key=user_key))
        
        for column in range(user_columns):
            start = column*user_rows
            end = (column+1)*user_rows
            self.canvas.saveState()
            self.canvas.translate(column*user_width, sheet_user_area_height - user_height + sheet_margin)
            for user in users[start:end]:
                self._draw_user(user)
                self.canvas.translate(0, -user_height)
            self.canvas.restoreState()
    
    def _draw_user(self, user):
        barcode_frame = platypus.Frame(x1=0, y1=0, width=user_width/2, height=user_height, showBoundary=1)
        mybarcode = code128.Code128(barWidth=units.inch * 0.015, value=user.get_barcode())
        mybarcode.humanReadable = 1
        barcode_frame.add(mybarcode, self.canvas)
        
        name_frame = platypus.Frame(x1=user_width/2, y1=0, width=user_width/2, height=user_height, showBoundary=1)
        style = styles.ParagraphStyle(name='Normal',
                                      fontName='Helvetica',
                                      fontSize=10,
                                      leading=12,
                                      allowOrphan=1)
        name_paragraph = platypus.Paragraph(u'<b>%s</b>' % user.get_name(), style)
        name_frame.add(name_paragraph, self.canvas)
        
        #self.canvas.setFont('Helvetica-Bold', user_label_size)
        #self.canvas.drawString(user_width/2, user_height/2, user.get_name())
        #self.canvas.setFont('Helvetica', user_label_size)
        #self.canvas.drawString(user_width/2, user_height/2 - user_label_size - 2, user.get_birthday())
        