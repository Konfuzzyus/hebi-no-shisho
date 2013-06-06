import database
import pygtk
pygtk.require('2.0')
import gtk

class ShishoApp():
    def __init__(self):
        database.init('data.db')
        self.window = MainWindow()

    def main(self):
        gtk.main()

class MainWindow():
    def __init__(self):
        self.gladefile = 'ShishoGUI.glade'
        self.builder = gtk.Builder() 
        self.builder.add_from_file(self.gladefile)
        
        dic = { "on_FileMenuQuit_activate" : gtk.main_quit}
        self.builder.connect_signals(dic, None)
        
        window = self.builder.get_object("MainWindow")
        window.show()
        return
