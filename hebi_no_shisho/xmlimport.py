import xml.etree.ElementTree as ET
import os

class ImportException(Exception):
    pass

class FileMakerXMLData:
    def __init__(self, filename):
        self.clear()
        self.ns = {'fmp': 'http://www.filemaker.com/fmpxmlresult'}
        
        print 'Loading FileMaker data from %(0)s' % {'0': filename}
        if os.path.isfile(filename):
            self.__tree = ET.parse(filename)
        else:
            raise ImportException('File %(0)s not found' % {'0': filename})
       
        self.__import_metadata()
        self.__import_resultset()
        
    def clear(self):
        self.__keys = []
        self.__data = []

    def __import_metadata(self):
        root = self.__tree.getroot()
        node = root.find('./fmp:METADATA', namespaces=self.ns)
        if node is None:
            raise ImportException('XML Data file does not contain a METADATA element')
        
        for field in node.findall('./fmp:FIELD', namespaces=self.ns):
            self.__keys.append(field.attrib['NAME'])
        print 'Found %(0)d keys: %(1)s' % {'0': len(self.__keys), '1': self.__keys}

    def __import_resultset(self):
        root = self.__tree.getroot()
        node = root.find('./fmp:RESULTSET', namespaces=self.ns)
        if node is None:
            raise ImportException('XML Data file does not contain a RESULTSET element')
        
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
            raise ImportException('ROW element needs to contain exactly %(0)d COL elements but contains only %(0)d COL elements') % {'0': len(columns), '1': len(self.__keys)}
        
        item = {}
        col_index = 0
        for col in columns:
            data = col.find('./fmp:DATA', namespaces=self.ns)
            if data is None:
                raise ImportException('DATA element missing from COL element')
            item[self.__keys[col_index]] = data.text
            col_index += 1
        self.__data.append(item)


#------------------------------------------------------------------------------
# Testing
#------------------------------------------------------------------------------
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def test_import(self):
        testfile = os.path.abspath(os.path.join('external_data', 'benutzer.xml'))
        FileMakerXMLData(testfile)
        testfile = os.path.abspath(os.path.join('external_data', 'ausleihe2.xml'))
        FileMakerXMLData(testfile)
        testfile = os.path.abspath(os.path.join('external_data', 'medien.xml'))
        FileMakerXMLData(testfile)
