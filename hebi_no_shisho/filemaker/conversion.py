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
import re

def _pull_item(row, key):
    item = ' '.join(row[key]).strip()
    if item == "":
        return None
    return item

def _convert_to_user_status(status, locked):
    if locked != '':
        return constants.USER_DELETED
    if status.find('Lehrer') != -1:
        return constants.USER_TEACHER
    return constants.USER_STUDENT

def _unmangle_signature(signature):
    if signature is None:
        return None, None
    if re.match('\d{3}([.]\d*)?', signature):
        return signature, None
    return None, signature

def extract_media(data):
    converted = []
    
    for row in data:
        entry = {}
        entry['barcode'] = _pull_item(row, 'Strichcode Medien')
        entry['isbn'] =  _pull_item(row, 'ISBN')
        entry['title'] =  _pull_item(row, 'Titel')
        entry['author'] = _pull_item(row, 'Urheber')
        entry['language'] = _pull_item(row, 'Sprache')
        entry['summary'] = None
        entry['subjects'] = _pull_item(row, 'Schlagwort')
        dewey, signature = _unmangle_signature(_pull_item(row, 'Signatur'))
        entry['dewey'] = dewey
        entry['signature'] = signature
        entry['publisher_name'] = _pull_item(row, 'Verlag')
        entry['notes'] = _pull_item(row, 'Bemerkungen')
        entry['edition'] = _pull_item(row, 'Auflage')
        entry['physical_description'] = None
        converted.append(entry)
    
    return converted

def extract_users(data):
    converted = []
    
    for row in data:
        entry = {}
        entry['first_name'] = _pull_item(row, 'Vorname')
        entry['last_name'] = _pull_item(row, 'Name')
        entry['form'] = _pull_item(row, 'Klasse')
        entry['barcode'] = _pull_item(row, 'Benutzercode')
        entry['birthday'] = None
        entry['status'] = _convert_to_user_status(_pull_item(row, 'Benutzerkategorie'), _pull_item(row, 'Benutzer_gesperrt'))
        converted.append(entry)
    
    return converted
    
