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

from hebi_no_shisho.filemaker import importer
from hebi_no_shisho.data import database
import unittest
import os
import tempfile

class TestMediaImporter(unittest.TestCase):

    def create_testfile(self, xml_data):
        handle, path = tempfile.mkstemp()
        os.write(handle, xml_data)
        os.close(handle)
        return path

    def setUp(self):
        self.__testbase = database.Database(':memory:')
        self.__testbase.reset_database('test')

    def test_demangle_isbn(self):
        testimporter = importer.MediaDataImporter(None)
        
        testcases = [
            ['0123-4567-89', '9780123456786'],
            ['0-571-08989-5', '9780571089895'],
            ['978-3841421050', '9783841421050'],
            [' 0-671657-15-1', '9780671657154'],
            ['0-671.65715-1', '9780671657154'],
            ['o-67l657-15-1', '9780671657154'],
            ['0.67,1657I5.1', '9780671657154'],
            ['O,671-65715-1', '9780671657154'],
            ['978O, 671- 65715-4', '9780671657154']
        ]
        
        for isbnstring, expected_isbn in testcases:
            self.assertEqual(expected_isbn, testimporter.demangle_isbn(isbnstring).isbn)
        
    def test_import_media(self):
        testimporter = importer.MediaDataImporter(self.__testbase)
        
        testdata = [{'barcode': '*433094*',
                     'isbn': '978-0060-57879-4',
                     'title': 'Printing Monkeys',
                     'author': 'Alfred Fredalf',
                     'language': 'eng.',
                     'summary': None,
                     'subjects': 'printing, primates',
                     'dewey': '999.999',
                     'publisher_name': 'Banana Prints',
                     'notes': None,
                     'edition': 'Paperback',
                     'physical_description': None},
                    {'barcode': '*412094*',
                     'isbn': '978-0-96426109-9',
                     'title': 'Frankenputer Assembly',
                     'author': 'Dr. Probble',
                     'language': 'eng.',
                     'summary': None,
                     'subjects': 'atrocities, technology',
                     'dewey': '999.999',
                     'publisher_name': 'Backdrop Ltd.',
                     'notes': 'Banned in 6 countries',
                     'edition': 'Hardcover',
                     'physical_description': None}]
        testimporter.import_data(testdata)