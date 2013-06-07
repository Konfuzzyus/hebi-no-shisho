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

from sqlobject import * #@UnusedWildImport
import os

from passlib.hash import sha256_crypt

class PermissionViolation(Exception):
    pass

class DatabaseIntegrityError(Exception):
    pass

class Database():
    __password_key = 'password'

    def __init__(self, filename):
        if filename == ':memory:':
            connection_string = 'sqlite:/:memory:'
        else:
            connection_string = 'sqlite:' + os.path.abspath(filename)
        sqlhub.processConnection = connectionForURI(connection_string)
    
    def erase_database(self):
        Book.dropTable(ifExists=True)
        Barcode.dropTable(ifExists=True)
        Student.dropTable(ifExists=True)
        Loan.dropTable(ifExists=True)
        Configuration.dropTable(ifExists=True)
    
    def reset_database(self, new_password):
        ''' Resets the database and sets a new password '''
        self.erase_database()
        self.create_tables()
        self.set_password(new_password)
        
    def set_password(self, new_password):
        ''' Sets the password in the database to a new one '''
        my_hash = sha256_crypt.encrypt(new_password)
        result = Configuration.select(Configuration.q.key == Database.__password_key)
        if result.count() == 0:
            Configuration(key=Database.__password_key, value=my_hash)
        else:
            result.getOne().value = my_hash
    
    def check_password(self, password):
        ''' Check whether the given password matches the one stored in the database '''
        try:
            result = Configuration.select(Configuration.q.key == Database.__password_key).getOne()
            return sha256_crypt.verify(password, result.value)
        except SQLObjectNotFound:
            raise DatabaseIntegrityError('Password entry missing from configuration table')
    
    def is_valid(self):
        ''' Check whether the database is ready for use '''
        if not Book.tableExists():
            return False
        if not Barcode.tableExists():
            return False
        if not Student.tableExists():
            return False
        if not Loan.tableExists():
            return False
        if not Configuration.tableExists():
            return False
        result = Configuration.select(Configuration.q.key == Database.__password_key)
        if result.count() == 0:
            return False
        return True
    
    def create_tables(self):
        Configuration.createTable(ifNotExists=True)
        Book.createTable(ifNotExists=True)
        Barcode.createTable(ifNotExists=True)
        Student.createTable(ifNotExists=True)
        Loan.createTable(ifNotExists=True)

class Configuration(SQLObject):
    key = StringCol(notNone=True, unique=True)
    value = StringCol()

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


#------------------------------------------------------------------------------
# Testing
#------------------------------------------------------------------------------
import unittest

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.database = Database(':memory:')
        
    def test_database_setup(self):
        my_password = 'this_is_sparta'
        not_my_password = 'such_is_life'
        self.assertFalse(self.database.is_valid())
        self.database.reset_database(my_password)
        self.assertTrue(self.database.check_password(my_password))
        self.assertFalse(self.database.check_password(not_my_password))
        self.assertTrue(self.database.is_valid())