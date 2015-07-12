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

from PyQt5 import QtWidgets
from pybrarius.gui import mainwindow
from pybrarius.data import database
import os

class ShishoApplication(QtWidgets.QApplication):
    def __init__(self, *args, **kw):
        super(ShishoApplication, self).__init__(*args, **kw)
        
        self.__localpath = os.path.expanduser(os.path.join('~', '.hebi-no-shisho'))
        if not os.path.isdir(self.__localpath):
            os.makedirs(self.__localpath)
        
        self.__database = database.Database(os.path.join(self.__localpath, 'database.db'))
        self.__rootwindow = mainwindow.MainWindow(self.__database)

    def run(self):
        self.__rootwindow.show()
        return self.exec_()
