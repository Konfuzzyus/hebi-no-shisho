import database

class AppAdmin(object):
    def __init__(self):
        database.init()

    def run(self):
        database.createTables()