import database

class AppUser(object):


    def __init__(self):
        database.init()
        return

    def run(self):
        if not database.isValid():
            print 'The database is not in a valid state. Run the admin tool to address the issue.'
        return 0