## This library provides User Input fields

import gtk, pygtk, gobject

class LeftAlignedLabel(gtk.Alignment):
    
    def __init__(self, markup, left_padding=0):
        
        gtk.Alignment.__init__(self, 0,0.5,0,0)
        
        label = gtk.Label()
        label.set_markup("  "*left_padding + markup)

        self.add(label)
        label.show()

class UsernameField(gtk.Entry):
    
    def __init__(self, parent=None):
        
        gtk.Entry.__init__(self)

        self.set_text( "Utente" )


class PasswordField(gtk.Entry):
    
    def __init__(self, parent=None):
        
        gtk.Entry.__init__(self)

        self.set_text ("Password")
        self.set_visibility(False)

class AuthBlock(gtk.HBox):
    
    def __init__(self, default_spacing=5, left_padding=0):
        
        gtk.HBox.__init__(self)

        self.user_field = UsernameField()
        self.password_field = PasswordField()
        
        vbox1 = gtk.VBox()
        vbox2 = gtk.VBox()

        label = LeftAlignedLabel("Utente", 2)
        vbox1.pack_start( label )
        label.show()

        label = LeftAlignedLabel("Password", 2)
        vbox1.pack_start( label )
        label.show()

        vbox2.pack_start(self.user_field)
        vbox2.pack_start(self.password_field)

        self.user_field.show()
        self.password_field.show()

        self.pack_start(vbox1)
        self.pack_start(vbox2)

        vbox1.show()
        vbox2.show()

    def get_username(self):
        return self.user_field.get_text()

    def get_password(self):
        return self.password_field.get_text()

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
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
        if chooser.run() == gtk.RESPONSE_OK:
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

class PrinterSettingsBlock(gtk.HBox):
    
    def __init__(self, default_spacing = 5, left_padding=0):
         
        gtk.HBox.__init__(self)
        
        vbox1 = gtk.VBox(False, default_spacing)
        vbox2 = gtk.VBox(False, default_spacing)

        self.set_spacing(default_spacing)

        label = LeftAlignedLabel("Stampante", 2)
        vbox1.pack_start(label)
        label.show()

        self.printer_chooser = PrinterComboBox()
        vbox2.pack_start( self.printer_chooser )
        self.printer_chooser.show()

        label = LeftAlignedLabel("File", 2)
        vbox1.pack_start( label )
        label.show()

        self.select_file_widget = SelectFileWidget()
        vbox2.pack_start (self.select_file_widget)
        self.select_file_widget.show()

        label = LeftAlignedLabel("Pagine per foglio", 2)
        vbox1.pack_start(label)
        label.show()
        
        self.page_per_page = PagePerPageComboBox()
        vbox2.pack_start(self.page_per_page)
        self.page_per_page.show()

        self.pack_start(vbox1)
        self.pack_start(vbox2)

        vbox1.show()
        vbox2.show()

    def get_filename(self):
        return self.select_file_widget.GetFile()

    def get_printer(self):
        return self.printer_chooser.get_printer()

    def get_page_per_page(self):
        return self.page_per_page.get_page_per_page()



class PageRangeBlock(gtk.VBox):
    
    def __init__(self):
        
        gtk.VBox.__init__(self)

        self.check_button = gtk.CheckButton("Stampa solo una parte del documento",
                                       True)

        self.check_button.set_active(False)

        self.check_button.connect('clicked', self.check_button_callback)

        self.pack_start(self.check_button)
        self.check_button.show()

        self.hbox = gtk.HBox()
        
        self.range_field = gtk.Entry()

        label = LeftAlignedLabel("Range di pagine", 2)
        self.hbox.pack_start(label)
        self.hbox.pack_start(self.range_field)
        label.show()

        self.pack_start(self.hbox)

        self.range_field.show()

        self.hbox.show()
        self.hbox.set_spacing( 5 )
        self.hbox.set_sensitive(False)

    def check_button_callback(self, obj):
        
        if self.check_button.get_active() == False:
            self.hbox.set_sensitive(False)
        else:
            self.hbox.set_sensitive(True)

    def get_page_range(self):
        
        if self.check_button.get_active() == False:
            return None

        return self.range_field.get_text()

        
            

        
