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

from hebi_no_shisho.library import constants
from hebi_no_shisho.data import database
from datetime import datetime
import re


def _pull_item(row, key):
    item = ' '.join(row[key]).strip()
    if item == "":
        return None
    return item

def _convert_to_user_status(status, locked):
    if not locked is None:
        return constants.USER_DELETED
    if not status is None and status.find(u'Lehrer') != -1:
        return constants.USER_TEACHER
    return constants.USER_STUDENT

def _unmangle_signature(signature):
    if signature is None:
        return None, None
    if re.match('\d{3}([.]\d*)?', signature):
        return signature, None
    return None, signature

def _convert_date(raw_date):
    if raw_date is None:
        return raw_date
    parsed_date = datetime.strptime(raw_date, '%d.%m.%Y')
    return parsed_date.strftime(database.date_format)

def extract_media(data):
    converted = []
    
    for row in data:
        entry = {}
        barcode = _pull_item(row, u'Strichcode Medien')
        if not barcode is None:
            barcode = barcode.replace('*', '')
        entry['barcode'] = barcode
        entry['isbn'] =  _pull_item(row, u'ISBN')
        entry['title'] =  _pull_item(row, u'Titel')
        entry['author'] = _pull_item(row, u'Urheber')
        entry['language'] = _pull_item(row, u'Sprache')
        entry['summary'] = None
        entry['subjects'] = _pull_item(row, u'Schlagwort')
        dewey, signature = _unmangle_signature(_pull_item(row, u'Signatur'))
        entry['dewey'] = dewey
        entry['signature'] = signature
        entry['publisher_name'] = _pull_item(row, u'Verlag')
        entry['notes'] = _pull_item(row, u'Bemerkungen')
        entry['edition'] = _pull_item(row, u'Auflage')
        entry['physical_description'] = None
        converted.append(entry)
    
    return converted

def extract_users(data):
    converted = []
    
    for row in data:
        entry = {}
        entry['first_name'] = _pull_item(row, u'Vorname')
        entry['last_name'] = _pull_item(row, u'Name')
        entry['form'] = _pull_item(row, u'Klasse')
        barcode = _pull_item(row, u'Benutzercode')
        if not barcode is None:
            barcode = barcode.replace('*', '')
        entry['barcode'] = barcode
        entry['birthday'] = None
        entry['status'] = _convert_to_user_status(_pull_item(row, u'Benutzerkategorie'), _pull_item(row, 'Benutzer_gesperrt'))
        converted.append(entry)
    
    return converted
    

def extract_loans(data):
    converted = []
    
    for row in data:
        entry = {}
        entry['loanDate'] = _convert_date(_pull_item(row, u'Ausleihdatum'))
        entry['returnDate'] = _convert_date(_pull_item(row, u'Rückgabedatum'))
        entry['book_code'] = _pull_item(row, u'NR Zugang')
        entry['borrower_code'] = _pull_item(row, u'Ausleihperson')
        converted.append(entry)
    
    return converted
    