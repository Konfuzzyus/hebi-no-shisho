from sqlobject import * #@UnusedWildImport
import os

def init():
    connection_string = 'sqlite:' + os.path.abspath('data.db')
    sqlhub.processConnection = connectionForURI(connection_string)

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