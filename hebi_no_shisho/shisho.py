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
        
        self.builder = gtk.Builder() 
        self.builder.add_from_file('ShishoGUI.glade')
        
        self.setup_main()
        self.setup_about()
        self.setup_password_entry()
        
        self.win_main.show()

    def main(self):
        gtk.main()

        
    def setup_main(self):
        self.win_main = self.builder.get_object("winMain")
        self.win_main.connect("destroy", gtk.main_quit)
        dic = { "on_FileMenuQuit_activate" : gtk.main_quit,
                "on_FileMenuAdminMode_activate": self.enter_admin_mode,
                "on_HelpMenuAbout_activate": self.show_about}
        self.builder.connect_signals(dic, None)
        return

    def setup_about(self):
        self.win_about = self.builder.get_object("dlgAbout")
        
    def setup_password_entry(self):
        self.win_password = self.builder.get_object("dlgPasswordEntry")
        self.win_password_entry = self.builder.get_object("entPassword")
        self.win_password_label = self.builder.get_object("lblPasswordEntry")

    def enter_admin_mode(self, widget):
        if self.database.is_valid():
            self.win_password_label.set_text('Login')
            self.win_password_entry.set_text('')
            result = self.win_password.run()
            if result == 1:
                if self.database.check_password(self.win_password_entry.get_text()):
                    print 'Success!'
                else:
                    print 'FAIL'
        else:
            self.win_password_label.set_text('Create')
            result = self.win_password.run()
            if result == 1:
                self.database.reset_database(self.win_password_entry.get_text())
        self.win_password.hide()

    def show_about(self, widget):
        self.win_about.run()
        self.win_about.hide()
