## This library is part of DrPrintGui 
##
## This file provide the MainWin object,
## that is the main window of the DrPrint
## application

__author__ = 'Leonardo Robol <leo@robol.it>'

import gtk, pygtk

from Input import UsernameField, PasswordField, PrintButton, SelectFileWidget, PrinterComboBox

import paramiko

class MainWin(gtk.Window):
    """MainWin object for DrPrint"""

    def __init__(self, parent=None):
        
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

        self.set_title = "DrPrint 0.1"
        self.set_border_width(10)

        self.default_spacing = 5

        self.connect('destroy' , gtk.main_quit)

        self.build()

        self.connect_all()

    def build(self):
        """This function builds up the interface using pieces
        from DrPrintGui"""

        # The main LayOut VBox
        layout_box = gtk.VBox()
        layout_box.set_spacing( self.default_spacing )
        
        # The authentication Input
        authentication_box = gtk.HBox()
        authentication_box.set_spacing( self.default_spacing )

        self.user_field = UsernameField()
        authentication_box.pack_start(self.user_field, 1)
        self.user_field.show()

        self.password_field = PasswordField()
        authentication_box.pack_start(self.password_field, 1)
        self.password_field.show()

        self.print_button = PrintButton()
        authentication_box.pack_start(self.print_button, 1)
        self.print_button.show()

        layout_box.pack_start ( authentication_box )
        authentication_box.show()

        # The PDF file loading and print settings
        file_chooser_box = gtk.HBox()
        file_chooser_box.set_spacing ( self.default_spacing )
        
        self.select_file_widget = SelectFileWidget()
        file_chooser_box.pack_start( self.select_file_widget )
        self.select_file_widget.show()

        self.printer_chooser = PrinterComboBox()
        file_chooser_box.pack_start(self.printer_chooser)
        self.printer_chooser.show()
        
        layout_box.pack_start (file_chooser_box)

       
        file_chooser_box.show()

        

        self.add (layout_box)
        layout_box.show()


    def connect_all(self):
        self.print_button.connect('clicked', self.print_button_clicked_callback)

    def print_button_clicked_callback(self, widget):
        self.send_print()
    
    def send_print(self):
        # Get printer name
        printer = self.printer_chooser.get_printer()
        print "Select printer: %s" % printer
        
        # Get connection
        client = paramiko.SSHClient()
        username = self.user_field.get_text()
        password = self.password_field.get_text()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect('ssh.dm.unipi.it', 
                       port=22, 
                       username=username,
                       password=password)

        channel = client.get_transport().open_session()

        filename = self.select_file_widget.GetFile()
        print "Printing %s" % filename
        f = open(filename, 'r')
        
        channel.exec_command("lpr -P%s" % printer)
        channel.sendall( f.read() )
        f.close()
        channel.close()
        

    def debug(self, text):
        print text
        

        
