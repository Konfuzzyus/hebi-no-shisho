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

from pybrarius.filemaker import importer
from pybrarius.data import database
from pybrarius.library import constants
import unittest
import os
import tempfile

class TestXMLDataImporter(unittest.TestCase):

    def create_testfile(self, xml_data):
        handle, path = tempfile.mkstemp()
        os.write(handle, xml_data)
        os.close(handle)
        return path

    def setUp(self):
        self.__testbase = database.Database(':memory:')
        self.__testbase.reset_database('test')

    def test_import_users(self):
        testimporter = importer.UserDataImporter(self.__testbase)
        testdata = [{'first_name' : 'Anna',
                     'last_name' : 'Aebersold',
                     'form' : '5b',
                     'barcode' : '*2344*',
                     'birthday' : '1990-1-1',
                     'status' : constants.USER_STUDENT},
                    {'first_name' : 'Bert',
                     'last_name' : 'Bontbuddle',
                     'form' : '2b',
                     'barcode' : '*1231*',
                     'birthday' : '1993-4-2',
                     'status' : constants.USER_STUDENT},
                    {'first_name' : 'Christopher',
                     'last_name' : 'Cesar',
                     'form' : '4b',
                     'barcode' : '*3456*',
                     'birthday' : '1976-2-7',
                     'status' : constants.USER_TEACHER}]
        testimporter.import_data(testdata)
