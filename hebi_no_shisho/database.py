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
        Media.dropTable(ifExists=True)
        User.dropTable(ifExists=True)
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
        if not Media.tableExists():
            return False
        if not User.tableExists():
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
        Media.createTable(ifNotExists=True)
        User.createTable(ifNotExists=True)
        Loan.createTable(ifNotExists=True)
    
    def add_user(self, **kwargs):
        User(**kwargs)

    def add_media(self, **kwargs):
        Media(**kwargs)

class Configuration(SQLObject):
    key = StringCol(notNone=True, unique=True)
    value = StringCol()

class Inventory(SQLObject):
    barcode = StringCol(unique=True, notNone=True)
    info = ForeignKey('Media', cascade=True, notNone=True)

class Media(SQLObject):
    title = StringCol(notNone=True)
    author = StringCol(notNone=False)
    isbn = StringCol(notNone=True, unique=True)

class User(SQLObject):
    first_name = StringCol(notNone=True)
    last_name = StringCol(notNone=True)
    form = StringCol(notNone=True)
    loans = MultipleJoin('Loan')
    barcode = StringCol(notNone=True, unique=True)

class Loan(SQLObject):
    book = ForeignKey('Media', cascade=True, unique=True, notNone=True)
    borrower = ForeignKey('User', cascade=False, notNone=True)
    loanDate = DateCol(notNone=True)
