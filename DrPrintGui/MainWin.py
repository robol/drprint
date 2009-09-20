## This library is part of DrPrintGui 
#  -*- coding: utf-8 -*-
## This file provide the MainWin object,
## that is the main window of the DrPrint
## application


__author__ = 'Leonardo Robol <leo@robol.it>'

import gtk, pygtk

from Input import AuthBlock, PrinterSettingsBlock, PrintButton, LeftAlignedLabel
from Dialogs import ErrorDialog

class MainWin(gtk.Window):
    """MainWin object for DrPrint"""

    def __init__(self, backend=None):

        self.backend = backend
        
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

        # Qualche istruzinoe preliminare
        label = gtk.Label()
        label.set_markup("<b>Come usare questo programma:</b>\n\
<b>1)</b> Inserire nome utente e password \n<b>2)</b> Scegliere il file da stampare e la\
 stampante \n<b>3)</b> Premere il tasto stampa")

        layout_box.pack_start( label )
        label.show()
        
        label = LeftAlignedLabel("<b>Autenticazione (sui computer dell'Aula 4)</b>")
        layout_box.pack_start( label )
        label.show()

        self.auth_block = AuthBlock(self.default_spacing, 10)
        layout_box.pack_start ( self.auth_block )
        self.auth_block.show()

        # The PDF file loading and print settings
        label = LeftAlignedLabel("<b>Configurazione stampante</b>")
        layout_box.pack_start(label)
        label.show()

        self.printer_settings_block = PrinterSettingsBlock(self.default_spacing)
        layout_box.pack_start(self.printer_settings_block)
        self.printer_settings_block.show()

        self.print_button = PrintButton()
        layout_box.pack_start(self.print_button)
        self.print_button.show()

       
        self.add (layout_box)
        layout_box.show()


    def connect_all(self):
        self.print_button.connect('clicked', self.print_button_clicked_callback)
        self.backend.connect('auth_failed', self.auth_failed_callback)

    def print_button_clicked_callback(self, widget):
        if not self.backend == None:
            printer = self.printer_settings_block.get_printer()
            username = self.auth_block.get_username()
            password = self.auth_block.get_password()
            filename = self.printer_settings_block.get_filename()
            page_per_page = self.printer_settings_block.get_page_per_page()

            self.backend.send_print(printer = printer,
                                    username = username,
                                    password = password,
                                    filename = filename,
                                    page_per_page = page_per_page)
        else:
            self.debug( "Sembra che non ci sia un backend attaccato\
 a questa interfaccia, quindi non faccio nulla")

    def auth_failed_callback(self, obj):
        """Questa funzione gestisce l'eventualità che utente
        e password siano errati"""
        self.debug("Autenticazione fallita")
        dialog = ErrorDialog("Autenticazione Fallita",
                             "<b>Autenticazione Fallita</b>\nLo username e la password forniti non sono\n\
corretti. L'autenticazione su ssh.dm.unipi.it\nnon è andata a buon fine.")
        dialog.run()
        dialog.destroy()
    
           

    def debug(self, text):
        print text
        

        
