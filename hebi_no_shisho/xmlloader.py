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

import xml.etree.ElementTree as ET
import os

class LoadException(Exception):
    pass

class FileMakerXMLData:
    def __init__(self, filename):
        self.clear()
        self.ns = {'fmp': 'http://www.filemaker.com/fmpxmlresult'}
        
        print 'Loading FileMaker data from %(0)s' % {'0': filename}
        if os.path.isfile(filename):
            self.__tree = ET.parse(filename)
        else:
            raise LoadException('File %(0)s not found' % {'0': filename})
       
        self.__import_metadata()
        self.__import_resultset()
        
    def clear(self):
        self.__keys = []
        self.__data = []
    
    def get_data(self):
        return self.__data

    def __import_metadata(self):
        root = self.__tree.getroot()
        node = root.find('./fmp:METADATA', namespaces=self.ns)
        if node is None:
            raise LoadException('XML Data file does not contain a METADATA element')
        
        for field in node.findall('./fmp:FIELD', namespaces=self.ns):
            self.__keys.append(field.attrib['NAME'])
        print 'Found %(0)d keys: %(1)s' % {'0': len(self.__keys), '1': self.__keys}

    def __import_resultset(self):
        root = self.__tree.getroot()
        node = root.find('./fmp:RESULTSET', namespaces=self.ns)
        if node is None:
            raise LoadException('XML Data file does not contain a RESULTSET element')
        
        num_rows = int(node.attrib['FOUND'])
        print 'Found result set containing %(0)d rows' % {'0': num_rows}
        num_loaded = 0
        for row in node.findall('./fmp:ROW', namespaces=self.ns):
            self.__import_row(row)
            num_loaded += 1
        print 'Loaded a total of %(0)d rows' % {'0': num_loaded}
        
    def __import_row(self, row):
        columns = row.findall('./fmp:COL', namespaces=self.ns)
        if len(columns) != len(self.__keys):
            raise LoadException('ROW element needs to contain exactly %(0)d COL elements but contains only %(1)d COL elements' % {'0': len(columns), '1': len(self.__keys)})
        
        item = {}
        col_index = 0
        for col in columns:
            data_list = []
            for data in col.findall('./fmp:DATA', namespaces=self.ns):
                data_list.append(data.text)
            item[self.__keys[col_index]] = data_list
            col_index += 1
        self.__data.append(item)


#------------------------------------------------------------------------------
# Testing
#------------------------------------------------------------------------------
import unittest
import tempfile

class TestFileMakerXMLData(unittest.TestCase):

    def create_testfile(self, xml_data):
        handle, path = tempfile.mkstemp()
        os.write(handle, xml_data)
        os.close(handle)
        return path
    
    def build_loader(self, xmlfile):
        return FileMakerXMLData(xmlfile)

    def test_valid_import(self):
        xml_data = """<?xml version="1.0" encoding="UTF-8" ?>
            <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
                <ERRORCODE>0</ERRORCODE>
                <PRODUCT BUILD="27/11/2002" NAME="FileMaker Pro" VERSION="6.0Dv4"/>
                <DATABASE DATEFORMAT="d.M.yyyy" LAYOUT="" NAME="B4Benutzer.fp5" RECORDS="1596" TIMEFORMAT="k:mm:ss "/>
                <METADATA>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Message" TYPE="TEXT"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Number" TYPE="NUMBER"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Timestamp" TYPE="DATE"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="5" NAME="Authors" TYPE="TEXT"/>
                </METADATA>
                <RESULTSET FOUND="3">
                    <ROW MODID="0" RECORDID="1">
                        <COL>
                            <DATA>This is some Text</DATA>
                        </COL>
                        <COL>
                            <DATA>42</DATA>
                        </COL>
                        <COL>
                            <DATA>1.12.2013</DATA>
                        </COL>
                        <COL>
                            <DATA>Alice</DATA>
                            <DATA>Bob</DATA>
                            <DATA>Dave</DATA>
                        </COL>
                    </ROW>
                    <ROW MODID="0" RECORDID="2">
                        <COL>
                            <DATA>This is some more Text</DATA>
                        </COL>
                        <COL>
                        </COL>
                        <COL>
                            <DATA>30.1.2012</DATA>
                        </COL>
                        <COL>
                            <DATA>Ed</DATA>
                        </COL>
                    </ROW>
                </RESULTSET>
            </FMPXMLRESULT>
        """
        
        path = self.create_testfile(xml_data)
        
        loader = FileMakerXMLData(path)
        data = loader.get_data()
        for row in data:
            self.assertTrue('Message' in row)
            self.assertTrue('Number' in row)
            self.assertTrue('Timestamp' in row)
            self.assertTrue('Authors' in row)
            self.assertEqual(4, len(row))
        
        self.assertEqual(data[0]['Message'], ['This is some Text'])
        self.assertEqual(data[0]['Number'], ['42'])
        self.assertEqual(data[0]['Timestamp'], ['1.12.2013'])
        self.assertEqual(data[0]['Authors'], ['Alice', 'Bob', 'Dave'])
        
        self.assertEqual(data[1]['Message'], ['This is some more Text'])
        self.assertEqual(data[1]['Number'], [])
        self.assertEqual(data[1]['Timestamp'], ['30.1.2012'])
        self.assertEqual(data[1]['Authors'], ['Ed'])
        
        os.remove(path)
        
    def test_missing_resultset(self):
        xml_data = """<?xml version="1.0" encoding="UTF-8" ?>
            <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
                <ERRORCODE>0</ERRORCODE>
                <PRODUCT BUILD="27/11/2002" NAME="FileMaker Pro" VERSION="6.0Dv4"/>
                <DATABASE DATEFORMAT="d.M.yyyy" LAYOUT="" NAME="B4Benutzer.fp5" RECORDS="1596" TIMEFORMAT="k:mm:ss "/>
                <METADATA>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Message" TYPE="TEXT"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Number" TYPE="NUMBER"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Timestamp" TYPE="DATE"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="5" NAME="Authors" TYPE="TEXT"/>
                </METADATA>
            </FMPXMLRESULT>
        """
        
        path = self.create_testfile(xml_data)
        self.assertRaises(LoadException, self.build_loader, (path))
        os.remove(path)

    def test_missing_metadata(self):
        xml_data = """<?xml version="1.0" encoding="UTF-8" ?>
            <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
                <ERRORCODE>0</ERRORCODE>
                <PRODUCT BUILD="27/11/2002" NAME="FileMaker Pro" VERSION="6.0Dv4"/>
                <DATABASE DATEFORMAT="d.M.yyyy" LAYOUT="" NAME="B4Benutzer.fp5" RECORDS="1596" TIMEFORMAT="k:mm:ss "/>
                <RESULTSET FOUND="3">
                    <ROW MODID="0" RECORDID="1">
                        <COL>
                            <DATA>This is some Text</DATA>
                        </COL>
                        <COL>
                            <DATA>42</DATA>
                        </COL>
                        <COL>
                            <DATA>1.12.2013</DATA>
                        </COL>
                        <COL>
                            <DATA>Alice</DATA>
                            <DATA>Bob</DATA>
                            <DATA>Dave</DATA>
                        </COL>
                    </ROW>
                </RESULTSET>
            </FMPXMLRESULT>
        """
        
        path = self.create_testfile(xml_data)
        self.assertRaises(LoadException, self.build_loader, (path))
        os.remove(path)
    
    def test_missing_col(self):
        xml_data = """<?xml version="1.0" encoding="UTF-8" ?>
            <FMPXMLRESULT xmlns="http://www.filemaker.com/fmpxmlresult">
                <ERRORCODE>0</ERRORCODE>
                <PRODUCT BUILD="27/11/2002" NAME="FileMaker Pro" VERSION="6.0Dv4"/>
                <DATABASE DATEFORMAT="d.M.yyyy" LAYOUT="" NAME="B4Benutzer.fp5" RECORDS="1596" TIMEFORMAT="k:mm:ss "/>
                <METADATA>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Message" TYPE="TEXT"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Number" TYPE="NUMBER"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="1" NAME="Timestamp" TYPE="DATE"/>
                    <FIELD EMPTYOK="YES" MAXREPEAT="5" NAME="Authors" TYPE="TEXT"/>
                </METADATA>
                <RESULTSET FOUND="3">
                    <ROW MODID="0" RECORDID="1">
                        <COL>
                            <DATA>This is some Text</DATA>
                        </COL>
                        <COL>
                            <DATA>42</DATA>
                        </COL>
                        <COL>
                            <DATA>Alice</DATA>
                            <DATA>Bob</DATA>
                            <DATA>Dave</DATA>
                        </COL>
                    </ROW>
                </RESULTSET>
            </FMPXMLRESULT>
        """
        
        path = self.create_testfile(xml_data)
        self.assertRaises(LoadException, self.build_loader, (path))
        os.remove(path)
    
    def test_file_not_found(self):
        path = self.create_testfile("Empty")
        os.remove(path)
        self.assertRaises(LoadException, self.build_loader, (path))
