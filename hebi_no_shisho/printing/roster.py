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

from reportlab.lib import units
from reportlab.lib import pagesizes

left_margin = units.cm * 2.5
other_margins = units.cm * 1.5
page_size = pagesizes.A4

class UserRoster():
    
    def __init__(self, userlist):
        self.userlist = userlist
        
    def write_pdf(self, filename):
        pass