# -*- coding: utf-8 -*-
## This library is part of DrPrintGui 
## This file provide the MainWin object,
## that is the main window of the DrPrint
## application


__author__ = 'Leonardo Robol <leo@robol.it>'

import gtk, pygtk
import os
import sys

from Input import AuthBlock, PrinterSettingsBlock, PrintButton, LeftAlignedLabel, \
     PageRangeBlock, OrientationSelect, SidesSelect, QueueButton
from Dialogs import ErrorDialog, MessageDialog, InfoDialog, QueueDialog, ProgressDialog
from DrPrintBackend import PrintingError

class MainWin(gtk.Window):
    """MainWin object for DrPrint"""

    def __init__(self, backend=None, user = None, filename = None):

        self.backend = backend
        self.user = user
        self.filename = filename
        
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title("DrPrint")

        self.set_title = "DrPrint 1.0-rc1"
        self.set_border_width(10)

        self.default_spacing = 5

        self.connect('destroy' , gtk.main_quit)

        self.build()

        self.connect_all()

    def build(self):
        """This function builds up the interface using pieces
        from DrPrintGui"""

        # The main Layout VBox
        layout_box = gtk.VBox()
        layout_box.set_spacing( self.default_spacing )

        # Inseriamo l'immagine di Dr Print
        image_file = "/usr/share/drprint/drprint_gui.png"
        try:
            os.stat(image_file)
        except OSError:
            image_file = "/usr/local/share/drprint/drprint_gui.png"
            try:
                os.stat(image_file)
            except OSError:
                image_file = "drprint_gui.png"
        drprint_img = gtk.image_new_from_file(image_file)

        # Qualche istruzinoe preliminare
        label = gtk.Label()
        label.set_markup("<b>Come usare questo programma:</b>\n\
<b>1)</b> Inserire nome utente e password \n<b>2)</b> Scegliere il file da stampare e la\
 stampante \n<b>3)</b> Premere il tasto stampa")

        hbox = gtk.HBox();
        hbox.show()
        hbox.set_spacing(self.default_spacing)

        hbox.pack_start(drprint_img)
        drprint_img.show()

        hbox.pack_start( label )
        label.show()

        layout_box.pack_start(hbox, 20)
        
        
        label = LeftAlignedLabel("<b>Autenticazione (sui computer dell'Aula 4)</b>")
        layout_box.pack_start(label)
        label.show()

        hosts = ['ssh.dm.unipi.it', 'ssh1.dm.unipi.it', 'ssh2.dm.unipi.it']
        self.auth_block = AuthBlock(self.default_spacing, 10, user = self.user,
                                    default_hosts = hosts)
        layout_box.pack_start(self.auth_block)
        self.auth_block.show()

        # The PDF file loading and print settings
        label = LeftAlignedLabel("<b>Configurazione stampante</b>")
        layout_box.pack_start(label)
        label.show()

        # Piano terra e secondo piano
        printers = ['cdcpt@printserver', 'cdcpp@printserver']

        # Le stampanti numerate
        printers.extend(map(lambda x : "cdc"+str(x), range(1,12)))

        # Togliamo la cdc2 che sembra non esistere
        printers.remove("cdc2")
        
        self.printer_settings_block = PrinterSettingsBlock(self.default_spacing,
                                                           filename = self.filename,
                                                           printers = printers)
        layout_box.pack_start(self.printer_settings_block)
        self.printer_settings_block.show()

        self.orientation_select = OrientationSelect()
        layout_box.pack_start(self.orientation_select)
        self.orientation_select.show()

        label = LeftAlignedLabel("<b>Configurazione Avanzata</b>")
        layout_box.pack_start(label)
        label.show()

        self.page_range_block = PageRangeBlock()
        layout_box.pack_start(self.page_range_block)
        self.page_range_block.show()
        
        label = LeftAlignedLabel( "<b>Fronte retro</b>" )
        layout_box.pack_start(label)
        label.show()

        self.sides_select = SidesSelect()
        layout_box.pack_start(self.sides_select)
        self.sides_select.show()

        # Bottoni finali, omogenei :)
        hbox = gtk.HBox(True)
        
        self.queue_button = QueueButton()
        hbox.pack_start(self.queue_button)
        self.queue_button.show()

        self.print_button = PrintButton()
        hbox.pack_start(self.print_button)
        self.print_button.show()
        
        layout_box.pack_start(hbox)
        hbox.show ()

       
        self.add (layout_box)
        layout_box.show()


    def connect_all(self):
        self.queue_button.connect('clicked', self.queue_button_clicked_callback)
        self.print_button.connect('clicked', self.print_button_clicked_callback)

    def queue_button_clicked_callback(self, widget):
        self.queue_button.set_state("running")
        printer = self.printer_settings_block.get_printer()
        username = self.auth_block.get_username()
        password = self.auth_block.get_password()
        remote_host = self.auth_block.get_remote_host()
        try:
            jobs = self.backend.get_queue(printer, remote_host, username, password)
        except RuntimeError, e:
            dialog = ErrorDialog("<b>Errore di connessione</b>",
                                 "Il seguente errore si è verificato durante il recupero della coda: %s" % e)
            resp = dialog.run()
            dialog.destroy()
            jobs = None
          
        # Se siamo riusciti a scucire qualche informazione la mostriamo,
        # altrimenti no.
        self.queue_button.set_state("idle")
        if jobs is not None:
	  qd = QueueDialog(jobs, printer)
	  resp = qd.run()
	  qd.destroy()
        
        

    def print_button_clicked_callback(self, widget):
        if not self.backend == None:

            # Comunichiamo all'utente che qualcosa sta succedendo
            self.print_button.set_state ("printing")
            
            printer = self.printer_settings_block.get_printer()
            username = self.auth_block.get_username()
            password = self.auth_block.get_password()
            filename = self.printer_settings_block.get_filename()
            page_per_page = self.printer_settings_block.get_page_per_page()
            page_range = self.page_range_block.get_page_range()
            copies = self.printer_settings_block.get_copies()
            orientation = self.orientation_select.get_orientation()
            sides = self.sides_select.get_sides_select()
            remote_host = self.auth_block.get_remote_host ()

            resp = gtk.RESPONSE_OK
            
            # Proviamo a salvare l'utente utilizzato. Se non ci si riesce
            # non ci lamentiamo troppo.
            try:
                with open(os.path.expanduser("~/.drprint"), "w") as handle:
                    handle.write(username)
            except OSError:
                pass

            if not (filename.lower().endswith("pdf") |
                    filename.lower().endswith("ps")  |
                    filename.lower().endswith("txt")):
                dialog = MessageDialog("Attenzione!",
                                       "Il file che hai scelto di stampare\n\
non sembra essere un file <b>PS</b>,\n\
un file <b>PDF</b> o un file di testo, e quindi \n\
probabilmente il programma non stamperà\n\
quello che vuoi.\n\
Se vuoi continuare premi OK")
                resp = dialog.run()
                dialog.destroy()
                

            if resp == gtk.RESPONSE_OK:
                try:
                    progress_dialog = ProgressDialog(filename)
                    self.backend.connect('transfer-started', lambda widget : progress_dialog.show())
                    self.backend.connect('transfer-progress', 
                                         lambda widget, a, b : progress_dialog.set_fraction(a * 1.0 / b))
                    self.backend.connect('transfer-finished', lambda widget : progress_dialog.hide())
                    progress_dialog.connect('transfer-cancelled', self.backend.cancel_transfer)
                    result = self.backend.send_print(printer = printer,
                                            username = username,
                                            password = password,
                                            filename = filename,
                                            page_per_page = page_per_page,
                                            page_range = page_range,
                                            copies = copies,
                                            orientation=orientation,
                                            sides = sides,
                                            remote_host = remote_host)
                except PrintingError, e:
                    # Comunichiamo il fallimento
                    dialog = ErrorDialog("<b>Errore di stampa</b>",
                                         "Il seguente errore si è verificato durante la stampa: %s." % e)
                    dialog.run()
                    dialog.destroy()
                else:
                    if not result:
                        dialog = InfoDialog("Stampa effettuata",
                                            "Il file %s è stato stampato correttamente sulla stampante <b>%s</b>."
                                            % (filename, printer))
                        dialog.run()
                        dialog.destroy()

            self.print_button.set_state("idle")
        else:
            self.debug( "Sembra che non ci sia un backend attaccato\
 a questa interfaccia, quindi non faccio nulla")

    
           

    def debug(self, text):
        print text
        

        
