## This library provides User Input fields

import gtk, pygtk, gobject

class UsernameField(gtk.Entry):
    
    def __init__(self, parent=None):
        
        gtk.Entry.__init__(self)

        self.set_text( "Utente" )


class PasswordField(gtk.Entry):
    
    def __init__(self, parent=None):
        
        gtk.Entry.__init__(self)

        self.set_text ("Password")
        self.set_visibility(False)

class PrintButton(gtk.Button):
    
    def __init__(self, parent=None):
        
        gtk.Button.__init__(self, "Stampa")


class SelectFileWidget(gtk.HBox):
    
    def __init__(self):
        gtk.HBox.__init__(self)
        self.set_spacing (5)

        self.Filename = gtk.Entry()
        self.Browser = gtk.Button("Seleziona File")

        self.Browser.connect('clicked', self.SelectFile)

        self.pack_start(self.Filename, 1)
        self.pack_start(self.Browser, 1)
        self.Filename.show()
        self.Browser.show()

    def SelectFile(self, window):
        
        chooser = gtk.FileChooserDialog(
            title = "Seleziona file da stampare",
            parent = None,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=("Cancel", 1, "OK", 2) )
        if chooser.run() == 2:
            self.Filename.set_text(chooser.get_filename())
        
        chooser.destroy()

    def GetFile(self):
        return self.Filename.get_text()

            
class PrinterComboBox(gtk.HBox):
    
    def __init__(self):
        
        gtk.HBox.__init__(self)
        self.combobox = gtk.combo_box_new_text()
        self.combobox.append_text("cdc7")
        self.combobox.append_text("cdcpt")

        self.combobox.set_active(1)

        self.pack_start( self.combobox )
        self.combobox.show()

    def get_printer(self):
        return self.combobox.get_active_text()


class PagePerPageComboBox(gtk.HBox):
    
    def __init__(self):
        gtk.HBox.__init__(self)
        self.combobox = gtk.combo_box_new_text()
        self.combobox.append_text("1")
        self.combobox.append_text("2")
        self.combobox.append_text("4")

        self.combobox.set_active(0)

        self.pack_start( self.combobox )
        self.combobox.show()

    def get_page_per_page(self):
        return self.combobox.get_active_text()
