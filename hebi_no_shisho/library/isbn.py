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

class IsbnError(Exception):
    pass

class Isbn():
    def __init__(self, string):
        scrubbed = scrub_isbn(string)
        if validate_isbn10(scrubbed):
            self.isbn = convert_isbn10_to_isbn13(scrubbed)
        elif validate_isbn13(scrubbed):
            self.isbn = scrubbed
        else:
            raise IsbnError('Invalid ISBN string')


isbn10_length = 10
isbn10_weigths = range(1, isbn10_length + 1)

isbn13_length = 13
isbn13_weigths = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1]

def convert_isbn10_to_isbn13(string):
    if not validate_isbn10(string):
        raise IsbnError('String is not a valid ISBN-10')
    number = '978' + string[:-1]
    return number + calculate_checksum_isbn13(number)

def scrub_isbn(isbn):
    """Removes hyphenation and leading/training whitespace from an isbn string.
    
    :param str isbn: The ISBN string to be scrubbed
    :rtype: ``str``
    :return: The original string stripped and without hyphenation
    """
    return isbn.replace('-', '').strip()

def calculate_checksum_isbn10(isbn10):
    """Calculate the expected_checksum character of an ISBN-10.
    
    :param str isbn10: ISBN-10 string without expected_checksum
    :rtype: ``str``
    :return: The expected_checksum character for the given ISBN-10 string
    :raise Isbn10Error: The string is not a valid ISBN-10 number
    
    """
    
    if len(isbn10) != isbn10_length - 1:
        raise IsbnError('Given ISBN string is invalid: length of %s is %d - should be %d' % (isbn10, len(isbn10), isbn10_length - 1))
    
    if not isbn10.isdigit():
        raise IsbnError('Given ISBN string is invalid: %s should contain numbers only' % (isbn10))
    
    products = [int(x) * y for x, y in zip(isbn10, isbn10_weigths[:-1])]
    check = sum(products) % 11
    return ('X' if check == 10 else str(check))

def validate_isbn10(isbn10):
    """Validate the given string according to ISBN-10 specifications.
    
    :param str isbn10: ISBN-10 string without hyphenation
    :rtype: ``bool``
    :return: ``True`` if the given string is a valid ISBN-10
    
    """
    
    if len(isbn10) != isbn10_length:
        return False
    
    if not isbn10[:-1].isdigit():
        return False
    
    if not isbn10[isbn10_length-1].isdigit() and not isbn10[isbn10_length-1] == 'X':
        return False
    
    products = [(10 if x == 'X' else int(x)) * y for x, y in zip(isbn10, isbn10_weigths)]
    return sum(products) % 11 == 0

def calculate_checksum_isbn13(isbn13):
    """Calculate the expected_checksum character of an ISBN-13.
    
    :param str isbn: ISBN-13 string without expected_checksum
    :rtype: ``str``
    :return: The expected_checksum character for the given ISBN-13 string
    :raise Isbn13Error: The string is not a valid ISBN-13 number
    
    """
    
    if len(isbn13) != isbn13_length - 1:
        raise IsbnError('Given ISBN string is invalid: length of %s is %d - should be %d' % (isbn13, len(isbn13), isbn13_length - 1))
    
    if not isbn13.isdigit():
        raise IsbnError('Given ISBN string is invalid: %s should contain numbers only' % (isbn13))

    products = [int(x) * y for x, y in zip(isbn13, isbn13_weigths[:-1])]
    check = (10 - sum(products) % 10) % 10
    return str(check)

def validate_isbn13(isbn13):
    """Validate the given string according to ISBN-13 specifications.
    
    :param str isbn: ISBN-13 string without hyphenation
    :rtype: ``bool``
    :return: ``True`` if the given string is a valid ISBN-13
    
    """
    
    if len(isbn13) != isbn13_length:
        return False
    
    if not isbn13.isdigit():
        return False
    
    products = [int(x) * y for x, y in zip(isbn13, isbn13_weigths)]
    return (sum(products) % 10) == 0
