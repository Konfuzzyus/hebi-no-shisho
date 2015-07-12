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

from pybrarius.filemaker import importer, conversion, xmlloader
from pybrarius.printing import roster
from PyQt5 import QtWidgets

class AdminWindow(QtWidgets.QDialog):

    def __init__(self, database):
        super(AdminWindow, self).__init__()
        self.__database = database

        self.__tabwidget = QtWidgets.QTabWidget(self)
        self.__tabwidget.addTab(LibraryReporter(database), "Library")
        self.__tabwidget.addTab(UserBrowser(database), "Users")
        self.__tabwidget.addTab(MediaBrowser(database), "Media")
        self.__tabwidget.addTab(DatabaseAdmin(database), "Database")
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.__tabwidget)
        
        self.setLayout(mainLayout)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Hebi-no-Shisho Administration")
        self.setMinimumSize(160, 160)
        self.resize(480, 320)

    def createActions(self):
        pass

    def createMenus(self):
        pass


class LibraryReporter(QtWidgets.QWidget):
    def __init__(self, database):
        super(LibraryReporter, self).__init__()
        self.__database = database


class UserBrowser(QtWidgets.QWidget):
    def __init__(self, database):
        super(UserBrowser, self).__init__()
        self.__database = database
        
        self.userCatalogueButton = QtWidgets.QPushButton('Create User Catalogue')
        self.userCatalogueButton.clicked.connect(self.createUserCatalogue)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.userCatalogueButton)
        self.setLayout(layout)
    
    def createUserCatalogue(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(parent=self,
                                                     directory='UserCatalogue.pdf',
                                                     caption='Choose where to store catalogue',
                                                     filter='User catalogue (*.pdf)')
        if filename:
            userlist = self.__database.get_userlist()
            myroster = roster.UserRoster(userlist)
            myroster.write_pdf(filename)


class MediaBrowser(QtWidgets.QWidget):
    def __init__(self, database):
        super(MediaBrowser, self).__init__()
        self.__database = database


class DatabaseAdmin(QtWidgets.QWidget):
    def __init__(self, database):
        super(DatabaseAdmin, self).__init__()
        self.__database = database
        
        self.eraseButton = QtWidgets.QPushButton('Erase Database')
        self.eraseButton.clicked.connect(self.eraseDatabase)
        self.importMediaButton = QtWidgets.QPushButton('Import Media')
        self.importMediaButton.clicked.connect(self.importMedia)
        self.importUserButton = QtWidgets.QPushButton('Import Users')
        self.importUserButton.clicked.connect(self.importUsers)
        self.importLoanButton = QtWidgets.QPushButton('Import Loans')
        self.importLoanButton.clicked.connect(self.importLoans)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.importMediaButton)
        layout.addWidget(self.importUserButton)
        layout.addWidget(self.importLoanButton)
        layout.addWidget(self.eraseButton)
        self.setLayout(layout)
    
    def eraseDatabase(self):
        answer = QtWidgets.QMessageBox.question(self,
                                            "Erase Database",
                                            "Clicking Yes will erase the current database.\n"
                                            "This can not be undone, are you sure you want to continue?",
                                            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            self.__database.erase_database()
            self.topLevelWidget().close()
    
    def importMedia(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Select file to Import',
                                                     filter='FileMaker export (*.xml)')
        if filename:
            try:
                loader = xmlloader.FileMakerXMLData(str(filename))
                mediaimporter = importer.MediaDataImporter(self.__database)
                converted = conversion.extract_media(loader.get_data())
                mediaimporter.import_data(converted)
            except xmlloader.LoadException as e:
                QtWidgets.QMessageBox.information(self,
                                              'Loading Error',
                                              e,
                                              QtWidgets.QMessageBox.Ok)
    
    def importUsers(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Select file to Import',
                                                     filter='FileMaker export (*.xml)')
        if filename:
            try:
                loader = xmlloader.FileMakerXMLData(str(filename))
                userimporter = importer.UserDataImporter(self.__database)
                converted = conversion.extract_users(loader.get_data())
                userimporter.import_data(converted)
            except xmlloader.LoadException as e:
                QtWidgets.QMessageBox.information(self,
                                              'Loading Error',
                                              e,
                                              QtWidgets.QMessageBox.Ok)
                
    def importLoans(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Select file to Import',
                                                     filter='FileMaker export (*.xml)')
        if filename:
            try:
                loader = xmlloader.FileMakerXMLData(str(filename))
                loanimporter = importer.LoanDataImporter(self.__database)
                converted = conversion.extract_loans(loader.get_data())
                loanimporter.import_data(converted)
            except xmlloader.LoadException as e:
                QtWidgets.QMessageBox.information(self,
                                              'Loading Error',
                                              e,
                                              QtWidgets.QMessageBox.Ok)
