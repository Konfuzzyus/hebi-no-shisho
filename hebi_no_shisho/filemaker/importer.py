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

from hebi_no_shisho.library import isbn
from hebi_no_shisho.data import database

class DataImportError(Exception):
    pass

class ISBNDemanglingError(Exception):
    pass

class MediaDataImporter:
    def __init__(self, database):
        self.__database = database
    
    def import_data(self, data):
        error_count = 0
        progress_count = 0
        
        self.__database.begin_transaction()
        for row in data:
            try:
                self._import_row(row)
            except DataImportError as error:
                print u'Unable to import %s: %s' % (row, error)
                error_count += 1
            except:
                self.__database.rollback_transaction()
                raise
            progress_count += 1
        self.__database.commit_transaction()
            
        print 'Failed to import %d of %d rows' % (error_count, len(data))
    
    def _import_row(self, row):
        if not 'isbn' in row or row['isbn'] is None:
            raise DataImportError('No ISBN number given')
        if not 'title' in row or row['title'] is None:
            raise DataImportError('No title given')
        
        isbnstring = row.pop('isbn')
        try:
            isbn = self.demangle_isbn(isbnstring)
        except ISBNDemanglingError as error:
            raise DataImportError(u'Failed to interpret ISBN number correctly: %s' % error)
        barcode = row.pop('barcode')
        try:
            self.__database.add_book_information(isbn=isbn.isbn, **row)
        except UnicodeEncodeError as error:
            print 'Failed to encode %s' % row
            raise
        try:
            self.__database.add_book_exemplary(barcode=barcode, isbn=isbn.isbn)
        except database.DatabaseIntegrityError as error:
            raise DataImportError('Unable to add book to database: %s' % error)
    
    def demangle_isbn(self, isbnstring):
        # Fix (some) obvious typos
        fixed = isbnstring.replace('x', 'X')
        fixed = fixed.replace('o', '0')
        fixed = fixed.replace('O', '0')
        fixed = fixed.replace(',', '')
        fixed = fixed.replace('.', '-')
        fixed = fixed.replace(' ', '')
        fixed = fixed.replace('l', '1')
        fixed = fixed.replace('I', '1')
        
        # Check if the number is valid as is
        try:
            return isbn.Isbn(fixed)
        except isbn.IsbnError:
            pass
        
        # Maybe it is an ISBN13 that is missing the 978 prefix
        try:
            return isbn.Isbn('978' + fixed)
        except isbn.IsbnError:
            pass
        
        raise ISBNDemanglingError('%s is not a valid ISBN number' % isbnstring)

class UserDataImporter:
    def __init__(self, database):
        self.__database = database
    
    def import_data(self, data):
        error_count = 0
        progress_count = 0
        
        self.__database.begin_transaction()
        for row in data:
            try:
                self._import_row(row)
            except DataImportError as error:
                print u'Unable to import %s: %s' % (row, error)
                error_count += 1
            except:
                self.__database.rollback_transaction()
                raise
            progress_count += 1
        self.__database.commit_transaction()
            
        print 'Failed to import %d of %d rows' % (error_count, len(data))
    
    def _import_row(self, row):
        if not 'first_name' in row or row['first_name'] is None:
            raise DataImportError('No first name given')
        if not 'last_name' in row or row['last_name'] is None:
            raise DataImportError('No last name given') 
        
        try:
            self.__database.add_user(**row)
        except database.DatabaseIntegrityError as error:
            raise DataImportError('Unable to add user to database: %s' % error)
    
    
class LoanDataImporter:
    def __init__(self, database):
        self.__database = database
    
    def import_data(self, data):
        error_count = 0
        progress_count = 0
        
        self.__database.begin_transaction()
        for row in data:
            try:
                self._import_row(row)
            except DataImportError as error:
                print u'Unable to import %s: %s' % (row, error)
                error_count += 1
            except:
                self.__database.rollback_transaction()
                raise
            progress_count += 1
        self.__database.commit_transaction()
            
        print 'Failed to import %d of %d rows' % (error_count, len(data))
    
    def _import_row(self, row):
        if not 'book_code' in row or row['book_code'] is None:
            raise DataImportError('No book id given')
        if not 'borrower_code' in row or row['borrower_code'] is None:
            raise DataImportError('No borrower id given') 
        
        try:
            self.__database.add_loan(**row)
        except database.DatabaseIntegrityError as error:
            raise DataImportError('Unable to add loan to database: %s' % error)
    