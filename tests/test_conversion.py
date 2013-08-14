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

from hebi_no_shisho.filemaker import conversion
import unittest

class TestXMLDataImporter(unittest.TestCase):

    def test_convert_date(self):
        test_data = [ ['13.1.2013', '2013-01-13'],
                      ['2.2.1993', '1993-02-02'],
                      [None, None] ]
        for case in test_data:
            self.assertEquals(conversion._convert_date(case[0]), case[1])
