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
from hebi_no_shisho.data import userlist
from hebi_no_shisho.library import constants

from passlib.hash import sha256_crypt

date_format = '%Y-%m-%d'

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
        self.__transaction = None
    
    def erase_database(self):
        Media.dropTable(ifExists=True)
        Inventory.dropTable(ifExists=True)
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
        if not Inventory.tableExists():
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
        Inventory.createTable(ifNotExists=True)
    
    def add_user(self, first_name, last_name, **kwargs):
        result = User.select(AND(User.q.first_name == first_name,User.q.last_name == last_name), connection=self._get_transaction()).getOne(None)
        try:
            if result is None:
                User(first_name=first_name, last_name=last_name, connection=self._get_transaction(), **kwargs)
            else:
                result.set(connection=self._get_transaction(), **kwargs)
        except dberrors.DuplicateEntryError:
            raise DatabaseIntegrityError('Given barcode already exists in database')

    def add_loan(self, book_code, borrower_code, **kwargs):
        borrower = User.select(User.q.barcode == borrower_code, connection=self._get_transaction()).getOne(None)
        if borrower is None:
            raise DatabaseIntegrityError('Given borrower not present in database')
        book = Inventory.select(Inventory.q.barcode == book_code, connection=self._get_transaction()).getOne(None)
        if book is None:
            raise DatabaseIntegrityError('Given book not present in database')
        Loan(bookID=book.id, borrowerID=borrower.id, connection=self._get_transaction(), **kwargs)

    def add_book_information(self, isbn, **kwargs):
        result = Media.select(Media.q.isbn == isbn, connection=self._get_transaction()).getOne(None)
        if result is None:
            Media(isbn=isbn, connection=self._get_transaction(), **kwargs)
        else:
            result.set(**kwargs)

    def add_book_exemplary(self, barcode, isbn):
        result = Media.select(Media.q.isbn == isbn, connection=self._get_transaction()).getOne(None)
        if result is None:
            raise DatabaseIntegrityError('Requested ISBN information missing from database')
        try:
            Inventory(barcode=barcode, infoID=result.id, connection=self._get_transaction())
        except dberrors.DuplicateEntryError:
            raise DatabaseIntegrityError('Given barcode already exists in database')
    
    def is_on_loan(self, book_code):
        book = Inventory.select(Inventory.q.barcode == book_code, connection=self._get_transaction()).getOne(None)
        if book is None:
            raise DatabaseIntegrityError('Given barcode is not present in database')
        loans = Loan.select(AND(Loan.q.book == book.id, Loan.q.returnDate == None))
        if loans.count() > 0:
            return True
        return False
    
    def get_userlist(self):
        mylist = userlist.UserList()
        query = User.select(User.q.status != constants.USER_DELETED, orderBy=User.q.form)
        for result in query:
            username = u'%s %s' % (result.first_name, result.last_name)
            mylist.add_user(form=result.form,
                            usertype=result.status,
                            name=username,
                            birthday=result.birthday,
                            barcode=result.barcode)
        return mylist
    
    def _get_transaction(self):
        if self.__transaction is None:
            return sqlhub.getConnection()
        else:
            return self.__transaction
    
    def begin_transaction(self):
        if not self.__transaction is None:
            raise PermissionViolation('Started a new transaction when there already was one in progress')
        self.__transaction = sqlhub.getConnection().transaction()
    
    def commit_transaction(self):
        self.__transaction.commit(close=True)
        self.__transaction = None
    
    def rollback_transaction(self):
        self.__transaction.rollback()
        self.__transaction = None

class Configuration(SQLObject):
    key = StringCol(notNone=True, unique=True)
    value = UnicodeCol()

class Inventory(SQLObject):
    barcode = StringCol(unique=True, notNone=True)
    info = ForeignKey('Media', cascade=True, notNone=True)

class Media(SQLObject):
    isbn = StringCol(notNone=True, unique=True)
    title = UnicodeCol(notNone=True)
    author = UnicodeCol(notNone=False)
    language = StringCol(notNone=False)
    summary = UnicodeCol(notNone=False)
    subjects = UnicodeCol(notNone=False)
    dewey = StringCol(notNone=False)
    signature = UnicodeCol(notNone=False)
    publisher_name = UnicodeCol(notNone=False)
    notes = UnicodeCol(notNone=False)
    edition = UnicodeCol(notNone=False)
    physical_description = UnicodeCol(notNone=False)

class User(SQLObject):
    first_name = UnicodeCol(notNone=True)
    last_name = UnicodeCol(notNone=True)
    birthday = DateCol(notNone=False)
    full_name_index = DatabaseIndex('first_name', 'last_name', 'birthday')
    form = UnicodeCol(notNone=False)
    loans = MultipleJoin('Loan')
    barcode = StringCol(notNone=True, unique=True)
    status = StringCol(notNone=True)

class Loan(SQLObject):
    book = ForeignKey('Media', cascade=True, notNone=True)
    borrower = ForeignKey('User', cascade=False, notNone=True)
    loanDate = DateCol(notNone=False)
    returnDate = DateCol(notNone=False)
