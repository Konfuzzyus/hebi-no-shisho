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

from hebi_no_shisho.data import database
from datetime import date

class OperationException(Exception):
    pass

class Librarian():
    def __init__(self, database):
        self.__database = database
    
    def borrow(self, book_code, borrower_code):
        try:
            is_loaned = self.__database.is_on_loan(book_code)
        except database.DatabaseIntegrityError:
            raise OperationException('Given book was not found in database')
        if is_loaned:
            raise OperationException('Given book is already loaned out')
        self.__database.add_loan(book_code,
                                 borrower_code,
                                 loanDate=date.today(),
                                 returnDate=None)