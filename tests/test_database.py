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

import unittest

from hebi_no_shisho import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.database = database.Database(':memory:')
        
    def test_database_setup(self):
        my_password = 'this_is_sparta'
        not_my_password = 'such_is_life'
        self.assertFalse(self.database.is_valid())
        self.database.reset_database(my_password)
        self.assertTrue(self.database.check_password(my_password))
        self.assertFalse(self.database.check_password(not_my_password))
        self.assertTrue(self.database.is_valid())