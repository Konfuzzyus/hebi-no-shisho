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

from hebi_no_shisho.library import constants

class User():
    def __init__(self, name, birthday, barcode):
        self.name = name
        self.birthday = birthday
        self.barcode = barcode
    
    def get_name(self):
        return self.name
    
    def get_birthday(self):
        if self.birthday is None:
            return '---'
        return self.birthday
    
    def get_barcode(self):
        return self.barcode

class Form():
    def __repr__(self):
        return '%s (%d:%d)' % (self.get_name(), len(self.get_teachers()), len(self.get_pupils()))
    
    def __init__(self, name):
        self.name = name
        self.teachers = []
        self.pupils = []
    
    def get_teachers(self):
        return self.teachers
    
    def get_pupils(self):
        return self.pupils
    
    def get_name(self):
        if self.name is None:
            return u'Administration'
        return self.name
    
    def add_teacher(self, user):
        self.teachers.append(user)
    
    def add_pupil(self, user):
        self.pupils.append(user)

class UserList():
    def __repr__(self):
        message = ''
        for form in self.forms:
            message += '%s\n' % form
        return message
    
    def __init__(self):
        self.forms = {}
    
    def get_forms(self):
        return self.forms.values()
    
    def add_user(self, form, usertype, name, birthday, barcode):
        if not form in self.forms:
            self.forms[form] = Form(form)
        user = User(name, birthday, barcode)
        if usertype == constants.USER_TEACHER:
            self.forms[form].add_teacher(user)
        else:
            self.forms[form].add_pupil(user)
            