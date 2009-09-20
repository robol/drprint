## This library is part of DrPrintGui 
##
## This file provide the MainWin object,
## that is the main window of the DrPrint
## application

__author__ = 'Leonardo Robol <leo@robol.it>'

import gtk, pygtk

from Input import UsernameField, PasswordField, PrintButton, SelectFileWidget, PrinterComboBox, PagePerPageComboBox


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
        layout_box = gtk.Table(rows=9,columns=4)

        # Qualche istruzinoe preliminare
        label = gtk.Label()
        label.set_markup("<b>Come usare questo programma:</b>\n\
1) Inserire nome utente e password - 2) Scegliere il file da stampare e la\
 stampante - 3) Premere il tasto stampa")

        layout_box.attach(label, 0, 7, 0, 1)
        label.show()
        
        # The authentication Input (riga 1)
        for j in range(0, 8):
            layout_box.set_row_spacing( j , self.default_spacing )

        for j in range(0,2):
            layout_box.set_col_spacing( j , self.default_spacing )

        ## Un po' di spazio fra la spiegazione e la sostanza
        layout_box.set_row_spacing(0, 20)

        layout_box.set_homogeneous(False)

        label = gtk.Label()
        label.set_markup("<b>Autenticazione</b>")
        layout_box.attach( label, 0, 2, 1, 2 )
        label.show()

        label = gtk.Label("Utente")
        layout_box.attach( label, 0 , 1, 2 , 3)
        label.show()

        self.user_field = UsernameField()
        layout_box.attach( self.user_field, 1, 3, 2 , 3)
        self.user_field.show()

        label = gtk.Label("Password")
        layout_box.attach( label, 0, 1, 3, 4)
        label.show()

        self.password_field = PasswordField()
        layout_box.attach(self.password_field, 1, 3, 3, 4)
        self.password_field.show()

       
        # The PDF file loading and print settings
        label = gtk.Label()
        label.set_markup("<b>Configurazione stampante</b>")
        layout_box.attach(label, 0, 2, 4, 5)
        label.show()

        label = gtk.Label("Stampante")
        layout_box.attach(label, 0, 1, 5, 6)
        label.show()

        self.printer_chooser = PrinterComboBox()
        layout_box.attach( self.printer_chooser, 1, 3, 5, 6)
        self.printer_chooser.show()

        label = gtk.Label("File")
        layout_box.attach(label, 0, 1, 7, 8)
        label.show()

        self.select_file_widget = SelectFileWidget()
        layout_box.attach( self.select_file_widget, 1, 3, 7, 8)
        self.select_file_widget.show()

        self.print_button = PrintButton()
        layout_box.attach(self.print_button, 2, 3, 8, 9)
        self.print_button.show()

        label = gtk.Label("Pagine per foglio")
        layout_box.attach(label, 0, 1, 6, 7)
        label.show()
        
        self.page_per_page = PagePerPageComboBox()
        layout_box.attach(self.page_per_page, 1, 3, 6, 7)
        self.page_per_page.show()

        self.add (layout_box)
        layout_box.show()


    def connect_all(self):
        self.print_button.connect('clicked', self.print_button_clicked_callback)

    def print_button_clicked_callback(self, widget):
        if not self.backend == None:
            printer = self.printer_chooser.get_printer()
            username = self.user_field.get_text()
            password = self.password_field.get_text()
            filename = self.select_file_widget.GetFile()
            page_per_page = self.page_per_page.get_page_per_page()

            self.backend.send_print(printer = printer,
                                    username = username,
                                    password = password,
                                    filename = filename,
                                    page_per_page = page_per_page)
        else:
            self.debug( "Sembra che non ci sia un backend attaccato\
 a questa interfaccia, quindi non faccio nulla")
    
           

    def debug(self, text):
        print text
        

        
