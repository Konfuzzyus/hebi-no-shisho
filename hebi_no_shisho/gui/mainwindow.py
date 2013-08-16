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

from PyQt4 import QtGui
from hebi_no_shisho.gui import adminwindow
from hebi_no_shisho.library import librarian

class MainWindow(QtGui.QMainWindow):

    def __init__(self, database):
        super(MainWindow, self).__init__()
        self.__database = database

        self.createMainLayout()
        self.createActions()
        self.createMenus()
        self.createAdminWindow()

        self.setWindowTitle("Hebi-no-Shisho")
        self.setMinimumSize(160, 160)
        self.resize(480, 320)
    
    def createMainLayout(self):
        operator = LibraryOperator(self.__database)
        self.setCentralWidget(operator)

    def createActions(self):
        self.actAdmin = QtGui.QAction("Administration",
                                      self,
                                      statusTip="Enter database administration mode",
                                      triggered=self.startAdministration)

        self.actExit = QtGui.QAction("&Quit",
                                     self,
                                     shortcut="Ctrl+Q",
                                     statusTip="Quit the application",
                                     triggered=self.close)

        self.actAbout = QtGui.QAction("About",
                                      self,
                                      statusTip="About Hebi-no-Shisho",
                                      triggered=self.showAbout)
        self.actAboutQt = QtGui.QAction("About Qt",
                                        self,
                                        statusTip="About Qt",
                                        triggered=self.showAboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.actAdmin)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)
        self.helpMenu.addAction(self.actAboutQt)
    
    def createAdminWindow(self):
        self.__admindialog = adminwindow.AdminWindow(self.__database)
        self.__admindialog.setModal(True)

    def startAdministration(self):
        diag = QtGui.QInputDialog()
        
        if self.__database.is_valid():
            prompt = "Enter password for existing database:"
            accessCheck = self.accessExistingDatabase
        else:
            prompt = "No valid database found, enter a password to create a new database:"
            accessCheck = self.accessNewDatabase
        entered_password, ok = diag.getText(self,
                                            "Administration Mode",
                                            prompt,
                                            mode=QtGui.QLineEdit.Password)
        if ok:
            if accessCheck(entered_password):
                self.__admindialog.show()

    def accessExistingDatabase(self, password):
        if self.__database.check_password(str(password)):
            return True
        else:
            QtGui.QMessageBox.information(self,
                                          "Access denied",
                                          "Invalid password entered",
                                          QtGui.QMessageBox.Ok)
            return False

    def accessNewDatabase(self, new_password):
        diag = QtGui.QInputDialog()
        entered_password, ok = diag.getText(self,
                                            "Administration Mode",
                                            "Please re-enter your password to confirm creation of the database:",
                                            mode=QtGui.QLineEdit.Password)
        if ok:
            if new_password == entered_password:
                self.__database.reset_database(str(new_password))
                return True
            else:
                QtGui.QMessageBox.information(self,
                                              "Database creation failure",
                                              "The passwords you entered did not match.",
                                              QtGui.QMessageBox.Ok)
                return False
        return False

    def showAbout(self):
        QtGui.QMessageBox.about(self,
                                "About Hebi-no-Shisho",
                                "<h3>Hebi-no-Shisho</h3>"
                                "Copyright (C) 2013 - Christian Meyer<br>"
                                "This program comes with ABSOLUTELY NO WARRANTY<br>"
                                "This is free software, and you are welcome to redistribute it under certain conditions")

    def showAboutQt(self):
        QtGui.QMessageBox.aboutQt(self)

class LibraryOperator(QtGui.QWidget):
    def __init__(self, database):
        super(LibraryOperator, self).__init__()
        self.__librarian = librarian.Librarian(database)
        
        self.barcodeEntry = QtGui.QLineEdit('')
        self.barcodeEntry.returnPressed.connect(self.inputBarcode)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.barcodeEntry)
        layout.addStretch(1)
        self.setLayout(layout)
    
    def inputBarcode(self):
        try:
            code = str(self.barcodeEntry.text())
            self.__librarian.handleCode(code)
        except librarian.OperationException as error:
            QtGui.QMessageBox.information(self,
                                          "Inable to process barcode",
                                          "The librarian reported a problem while processing your barcode entry: %s" % error,
                                           QtGui.QMessageBox.Ok)
        self.barcodeEntry.clear()