# -*- coding: utf-8 -*-
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
                if not data.text is None:
                    data_list.append(data.text)
            item[self.__keys[col_index]] = data_list
            col_index += 1
        self.__data.append(item)

