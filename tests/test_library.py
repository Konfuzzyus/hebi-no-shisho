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

import unittest
from pybrarius.library import librarian, constants
from pybrarius.data import database

testUser = {'first_name' : 'Anna',
            'last_name' : 'Aebersold',
            'form' : '5b',
            'barcode' : '2344',
            'birthday' : '1990-1-1',
            'status' : constants.USER_STUDENT}
    
testInformation = {'isbn': '9780060578794',
                   'title': 'Printing Monkeys',
                   'author': 'Alfred Fredalf',
                   'language': 'eng.',
                   'summary': None,
                   'subjects': 'printing, primates',
                   'dewey': '999.999',
                   'signature': 'DALF',
                   'publisher_name': 'Banana Prints',
                   'notes': None,
                   'edition': 'Paperback',
                   'physical_description': None}
    
testExemplary = {'barcode': '433094',
                 'isbn': '9780060578794'}

class TestLibrarian(unittest.TestCase):
    
    def setUp(self):
        self.database = database.Database(':memory:')
        self.database.reset_database('test')
        self.database.add_book_information(**testInformation)
        self.database.add_user(**testUser)
        self.database.add_book_exemplary(**testExemplary)

    def test_borrowing(self):
        testlibrarian = librarian.Librarian(self.database)
        with self.assertRaisesRegexp(librarian.OperationException, 'Given book was not found in database'):
            testlibrarian.borrow(book_code='1111', borrower_code=testUser['barcode'])
        testlibrarian.borrow(book_code=testExemplary['barcode'], borrower_code=testUser['barcode'])
        with self.assertRaisesRegexp(librarian.OperationException, 'Given book is already loaned out'):
            testlibrarian.borrow(book_code=testExemplary['barcode'], borrower_code=testUser['barcode'])