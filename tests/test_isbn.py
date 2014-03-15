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
from pybrarius.library import isbn

class TestIsbn(unittest.TestCase):

    def test_calculate_checksum_isbn10(self):
        test_cases = [
            ['006224012', '9'],
            ['037602067', '9'],
            ['155652998', '8'],
            ['087348754', '0'],
            ['037353461', '2'],
            ['159486758', '5'],
            ['089042556', '6'],
            ['193912400', 'X']
        ]
        for number, expected_checksum in test_cases:
            self.assertEqual(isbn.calculate_checksum_isbn10(number), expected_checksum)

    
    def test_calculate_checksum_exceptions_isbn10(self):
        test_cases = [
            ['0x4343', 'Given ISBN string is invalid: length of 0x4343 is 6 - should be 9'],
            ['0123-45678b', 'Given ISBN string is invalid: length of 0123-45678b is 11 - should be 9'],
            ['01234567B', 'Given ISBN string is invalid: 01234567B should contain numbers only'],
            ['01ABC129-', 'Given ISBN string is invalid: 01ABC129- should contain numbers only'],
            ['xxxxxxxx1', 'Given ISBN string is invalid: xxxxxxxx1 should contain numbers only'],
        ]
        for string, expected_message in test_cases:
            with self.assertRaisesRegexp(isbn.IsbnError, expected_message):
                isbn.calculate_checksum_isbn10(string)

        
    def test_validate_isbn10(self):
        test_cases = [
            ['0062240129', True],
            ['0376020679', True],
            ['1556529988', True],
            ['0873487540', True],
            ['0373534612', True],
            ['1594867585', True],
            ['0890425566', True],
            ['0890425561', False],
            ['193912400X', True],
            ['1939124003', False],
            ['9781479186723', False],
            ['97814791', False],
            ['155652998B', False],
            ['ABCDEFGHI5', False]
        ]
        for number, expected_result in test_cases:
            self.assertEqual(isbn.validate_isbn10(number), expected_result, 'Validation result of %s != %s' % (number, expected_result))

    
    def test_calculate_checksum_isbn13(self):
        test_cases = [
            ['978144052588', '9'],
            ['978006057879', '4'],
            ['978007147703', '1'],
            ['978096426109', '9'],
            ['978158270223', '0'],
            ['978147918672', '3'],
            ['978078945728', '8']
        ]
        for number, expected_checksum in test_cases:
            self.assertEqual(isbn.calculate_checksum_isbn13(number), expected_checksum)

    
    def test_calculate_checksum_exceptions_isbn13(self):
        test_cases = [
            ['0x4343', 'Given ISBN string is invalid: length of 0x4343 is 6 - should be 12'],
            ['0123-45678b1129', 'Given ISBN string is invalid: length of 0123-45678b1129 is 15 - should be 12'],
            ['01234567B122', 'Given ISBN string is invalid: 01234567B122 should contain numbers only'],
            ['01ABC129-123', 'Given ISBN string is invalid: 01ABC129-123 should contain numbers only'],
            ['xxxxxxxxxxx1', 'Given ISBN string is invalid: xxxxxxxxxxx1 should contain numbers only'],
        ]
        for string, expected_message in test_cases:
            with self.assertRaisesRegexp(isbn.IsbnError, expected_message):
                isbn.calculate_checksum_isbn13(string)

    
    def test_validate_isbn13(self):
        test_cases = [
            ['9781440525889', True],
            ['9780060578794', True],
            ['9780071477031', True],
            ['9781582702230', True],
            ['9780964261099', True],
            ['9781479186723', True],
            ['978147918672X', False],
            ['9780789457288', True],
            ['9780789457282', False],
            ['0890425561', False],
            ['19391240077271', False],
            ['1939124003', False],
            ['9781479186721', False],
            ['97814791', False],
            ['15565299881-1', False],
            ['ABCDEFGHI5', False],
            ['9AV0964261099', False],
        ]
        for number, expected_result in test_cases:
            self.assertEqual(isbn.validate_isbn13(number), expected_result, 'Validation result of %s != %s' % (number, expected_result))
