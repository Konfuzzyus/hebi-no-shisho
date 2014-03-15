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

from pybrarius.filemaker import xmlloader
import unittest
import tempfile
import os

class TestFileMakerXMLData(unittest.TestCase):

    def create_testfile(self, xml_data):
        handle, path = tempfile.mkstemp()
        os.write(handle, xml_data)
        os.close(handle)
        return path
    
    def build_loader(self, xmlfile):
        return xmlloader.FileMakerXMLData(xmlfile)

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
        
        loader = xmlloader.FileMakerXMLData(path)
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
        self.assertRaises(xmlloader.LoadException, self.build_loader, (path))
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
        self.assertRaises(xmlloader.LoadException, self.build_loader, (path))
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
        self.assertRaises(xmlloader.LoadException, self.build_loader, (path))
        os.remove(path)
    
    def test_file_not_found(self):
        path = self.create_testfile("Empty")
        os.remove(path)
        self.assertRaises(xmlloader.LoadException, self.build_loader, (path))
