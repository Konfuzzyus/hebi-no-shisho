from sqlobject import * #@UnusedWildImport
import os

def init(filename):
    connection_string = 'sqlite:' + os.path.abspath(filename)
    sqlhub.processConnection = connectionForURI(connection_string)

def isValid():
    ''' Check whether the database is ready for use '''
    if not Book.tableExists():
        return False
    if not Barcode.tableExists():
        return False
    if not Student.tableExists():
        return False
    if not Loan.tableExists():
        return False
    return True

def createTables():
    Book.createTable(ifNotExists=True)
    Barcode.createTable(ifNotExists=True)
    Student.createTable(ifNotExists=True)
    Loan.createTable(ifNotExists=True)

class Book(SQLObject):
    title = StringCol(notNone=True)
    author = StringCol()
    isbn = StringCol(notNone=True, unique=True)
    barcode = ForeignKey('Barcode', cascade='null')
    onLoan = SingleJoin('Loan')

class Barcode(SQLObject):
    code = StringCol(notNone=True, unique=True)

class Student(SQLObject):
    name = StringCol(notNone=True)
    form = StringCol(notNone=True)
    barcode = ForeignKey('Barcode', cascade='null')
    loans = MultipleJoin('Loan')

class Loan(SQLObject):
    book = ForeignKey('Book', cascade=True, unique=True, notNone=True)
    borrower = ForeignKey('Student', cascade=False, notNone=True)
    loanDate = DateCol(notNone=True)
