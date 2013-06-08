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

class XMLDataImporter:
    def __init__(self, database):
        self.__database = database

    def import_users(self, xmldata):
        for user in xmldata:
            try:
                self.__database.add_user(first_name=' '.join(user['Vorname']),
                                         last_name=' '.join(user['Name']),
                                         form=' '.join(user['Klasse']),
                                         barcode=' '.join(user['Benutzercode']))
            except:
                raise

    def import_media(self, xmldata):
        for media in xmldata:
            try:
                self.__database.add_media(title=' '.join(media['Titel']),
                                          author=' '.join(media['Urheber']),
                                          isbn=' '.join(media['ISBN']),
                                          barcode=' '.join(media['Strichcode Medien']))
            except:
                raise

    def import_loans(self, xmldata):
        pass


#------------------------------------------------------------------------------
# Testing
#------------------------------------------------------------------------------
import unittest
import database
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
        importer = XMLDataImporter(self.__testbase)
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
        importer.import_users(testdata)
        
    def test_import_media(self):
        importer = XMLDataImporter(self.__testbase)
        testdata = [ {'Titel': ['Sellbester'],
                      'Urheber': ['Money Maggins'],
                      'Verlag': ['Monkeyprint'],
                      'ISBN': ['1-1111-1111-11'],
                      'Datum der Aufnahme': ['1.1.2013'],
                      'Signatur': ['MAGG'],
                      'Schlagwort': ['Money Fame'],
                      'Sprache': ['Eng.'],
                      'Strichcode Medien': ['*1234*']
                     },
                     {'Titel': ['The Hobby'],
                      'Urheber': ['Jake Shmolkins'],
                      'Verlag': ['Deep Pedigree'],
                      'ISBN': ['2-1111-1111-11'],
                      'Datum der Aufnahme': ['1.1.2013'],
                      'Signatur': ['SMOL'],
                      'Schlagwort': ['Hobby Selfmade'],
                      'Sprache': ['Eng.'],
                      'Strichcode Medien': ['*2234*']
                      }
                    ]
        importer.import_media(testdata)