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

class XMLDataImportError(Exception):
    pass

class ISBNDemanglingError(Exception):
    pass

class FileMakerXMLDataImporter:
    def __init__(self, database):
        self.__database = database

    def import_user_table(self, xmldata):
        error_count = 0
        progress_count = 0
        
        self.__database.begin_transaction()
        for row in xmldata:
            try:
                self.import_user_row(row)
            except XMLDataImportError as error:
                print "Unable to import %s: %s" % (row, error)
                error_count += 1
            except:
                self.__database.rollback_transaction()
                raise
            progress_count += 1
        self.__database.commit_transaction()
            
        print "Failed to import %d of %d rows" % (error_count, len(xmldata))
        
    def import_user_row(self, row):
        try:
            self.__database.add_user(first_name=' '.join(row['Vorname']),
                                     last_name=' '.join(row['Name']),
                                     form=' '.join(row['Klasse']),
                                     barcode=' '.join(row['Benutzercode']))
        except database.DatabaseIntegrityError as error:
            raise XMLDataImportError('Unable to add book to database: %s' % error)
    
    def import_media_table(self, xmldata):
        error_count = 0
        progress_count = 0
        
        self.__database.begin_transaction()
        for row in xmldata:
            try:
                self.import_media_row(row)
            except XMLDataImportError as error:
                print "Unable to import %s: %s" % (row, error)
                error_count += 1
            except:
                self.__database.rollback_transaction()
                raise
            progress_count += 1
        self.__database.commit_transaction()
            
        print "Failed to import %d of %d rows" % (error_count, len(xmldata))

    def import_loan_table(self, xmldata):
        pass


    def import_media_row(self, row):
        if not 'ISBN' in row or len(row['ISBN']) <= 0:
            raise XMLDataImportError('No ISBN number given')
        
        isbnstring = ' '.join(row['ISBN'])
        try:
            isbn = self.demangle_isbn(isbnstring)
        except ISBNDemanglingError as error:
            raise XMLDataImportError('Failed to interpret ISBN number correctly: %s' % error)
        
        self.__database.add_book_information(title=' '.join(row['Titel']),
                                             author=' '.join(row['Urheber']),
                                             isbn=' '.join(row['ISBN']))
        try:
            self.__database.add_book_exemplary(isbn=' '.join(row['ISBN']),
                                               barcode=' '.join(row['Strichcode Medien']))
        except database.DatabaseIntegrityError as error:
            raise XMLDataImportError('Unable to add book to database: %s' % error)
    
    def demangle_isbn(self, isbnstring):
        # Fix (some) obvious typos
        fixed = isbnstring.replace('x', 'X')
        fixed = fixed.replace('o', '0')
        fixed = fixed.replace('O', '0')
        fixed = fixed.replace(',', '-')
        fixed = fixed.replace('.', '-')
        fixed = fixed.replace(' ', '')
        
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
