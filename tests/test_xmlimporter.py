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

from hebi_no_shisho.filemaker import xmlimporter
from hebi_no_shisho.data import database
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

    def test_demangle_isbn(self):
        importer = xmlimporter.FileMakerXMLDataImporter(None)
        
        testcases = [
            ['0123-4567-89', '9780123456786'],
            ['0-571-08989-5', '9780571089895'],
            ['978-3841421050', '9783841421050'],
            [' 0-671657-15-1', '9780671657154'],
            ['0-671.65715-1', '9780671657154'],
            ['o-671657-15-1', '9780671657154'],
            ['0.67,165715.1', '9780671657154'],
            ['O,671-65715-1', '9780671657154'],
            ['978O, 671- 65715-4', '9780671657154']
        ]
        
        for isbnstring, expected_isbn in testcases:
            self.assertEqual(expected_isbn, importer.demangle_isbn(isbnstring).isbn)
        
    def test_import_users(self):
        importer = xmlimporter.FileMakerXMLDataImporter(self.__testbase)
        testdata = [ {'Name': ['Miller'],
                      'Vorname': ['Alice'],
                      'Klasse': ['B1a'],
                      'Nummer': ['12'],
                      'Strasse': ['Old Street'],
                      'PLZ': ['12345'],
                      'Wohnort': ['Testtown'],
                      'Lehrer': ['Stevenson'],
                      'Benutzercode': ['*54321*'],
                      'Bemerkungen': ['']
                     },
                     {'Name': ['Smith'],
                      'Vorname': ['Bob'],
                      'Klasse': ['B1a'],
                      'Nummer': ['13'],
                      'Strasse': ['New Street'],
                      'PLZ': ['12345'],
                      'Wohnort': ['Testtown'],
                      'Lehrer': ['Stevenson'],
                      'Benutzercode': ['*54322*'],
                      'Bemerkungen': ['']
                      }
                    ]
        importer.import_user_table(testdata)
        
    def test_import_media(self):
        importer = xmlimporter.FileMakerXMLDataImporter(self.__testbase)
        testdata = [ {'Titel': ['Sellbester'],
                      'Urheber': ['Money Maggins'],
                      'Verlag': ['Monkeyprint'],
                      'ISBN': ['978-00067-54022'],
                      'Datum der Aufnahme': ['1.1.2013'],
                      'Signatur': ['MAGG'],
                      'Schlagwort': ['Money Fame'],
                      'Sprache': ['Eng.'],
                      'Strichcode Medien': ['*1234*']
                     },
                     {'Titel': ['The Hobby'],
                      'Urheber': ['Jake Shmolkins'],
                      'Verlag': ['Deep Pedigree'],
                      'ISBN': ['978-00067-54023'],
                      'Datum der Aufnahme': ['1.1.2013'],
                      'Signatur': ['SMOL'],
                      'Schlagwort': ['Hobby Selfmade'],
                      'Sprache': ['Eng.'],
                      'Strichcode Medien': ['*2234*']
                      }
                    ]
        importer.import_media_table(testdata)