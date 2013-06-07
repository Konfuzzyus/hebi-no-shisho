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

import database
import pygtk
pygtk.require('2.0')
import gtk

class ShishoApp():
    def __init__(self):
        self.database = database.Database('data.db')
        self.window = MainWindow()

    def main(self):
        gtk.main()

class MainWindow():
    def __init__(self):
        self.gladefile = 'ShishoGUI.glade'
        self.builder = gtk.Builder() 
        self.builder.add_from_file(self.gladefile)
        
        dic = { "on_FileMenuQuit_activate" : gtk.main_quit}
        self.builder.connect_signals(dic, None)
        
        window = self.builder.get_object("winMain")
        window.show()
        return
