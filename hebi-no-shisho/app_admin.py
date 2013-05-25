import database

class AppAdmin(object):
    def __init__(self):
        database.init()

    def run(self):
        if not database.Book.tableExists():
            database.Book.createTable()
        return 0