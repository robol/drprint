# -*- coding: utf-8 -*-
## This library provides User Input fields

import os
from gi.repository import Gtk, GObject

class LeftAlignedLabel(Gtk.Alignment):
    
    def __init__(self, markup, left_padding=0):
        
        Gtk.Alignment.__init__(self)

	self.set_halign(0)
	self.set_valign(0.5)
        
        label = Gtk.Label()
        label.set_markup(markup)
        plw = PaddingLeftWidget(label, left_padding)

        self.add(plw)
        plw.show()

class PaddingLeftWidget(Gtk.Table):
    
    def __init__(self, widget, padding_left):
        
        Gtk.Table.__init__(self, 1, 2, False)
        label = Gtk.Label()
        self.set_col_spacing(0, padding_left)
        self.attach(label, 0,1,0,1, False, False)
        self.attach(widget, 1,2,0,1, False, False)
        
        label.show()
        widget.show()
        

class UsernameField(Gtk.Entry):
    
    def __init__(self, parent=None, user = None):
        
        Gtk.Entry.__init__(self)

        if user is None:
            self.set_text( os.getenv("USER") )
        else:
            self.set_text(user)		
	

class PasswordField(Gtk.Entry):
    
    def __init__(self, parent=None):
        
        Gtk.Entry.__init__(self)

        self.set_text ("")
        self.set_visibility(False)

class RemoteHostComboBox(Gtk.HBox):

    def __init__(self, default_hosts):

        Gtk.HBox.__init__(self)
        self.combobox = Gtk.ComboBoxText()
        for remote_host in default_hosts:
            self.combobox.append_text(remote_host)
            # Selezioniamo il primo host
            self.combobox.set_active(0)
            
        self.pack_start(self.combobox, True, True, 0)
        self.combobox.show()
    def get_remote_host(self):
        return self.combobox.get_active_text()

class AuthBlock(Gtk.HBox):
    
    def __init__(self, default_spacing=5, left_padding=0, user = None,
                 default_hosts = ['ssh.dm.unipi.it']):
        
        Gtk.HBox.__init__(self)

        self.user_field = UsernameField(user = user)
        self.password_field = PasswordField()
        
        vbox1 = Gtk.VBox(False, default_spacing)
        vbox2 = Gtk.VBox(False, default_spacing)

        label = LeftAlignedLabel("Server SSH", 20)
        vbox1.pack_start (label, True, True, 0)
        label.show ()
		
        if len(default_hosts) == 0:
            raise IndexError('Not remote hosts specified. Aborting')

        self.remote_host = RemoteHostComboBox(default_hosts)
        vbox2.pack_start(self.remote_host, True, True, 0)
        self.remote_host.show()
	
        label = LeftAlignedLabel("Utente", 20)
        vbox1.pack_start( label, True, True, 0 )
        label.show()

        label = LeftAlignedLabel("Password", 20)
        vbox1.pack_start( label, True, True, 0 )
        label.show()

        vbox2.pack_start(self.user_field, True, True, 0)
        vbox2.pack_start(self.password_field, True, True, 0)

        self.user_field.show()
        self.password_field.show()

        self.pack_start(vbox1, True, True, 0)
        self.pack_start(vbox2, True, True, 0)

        vbox1.show()
        vbox2.show()

        # If user is given give focus to password,
        # otherwise give focus to username
        if user is None:
            self.user_field.grab_focus ()
        else:
            self.password_field.grab_focus ()

    def get_username(self):
        return self.user_field.get_text()

    def get_password(self):
        return self.password_field.get_text()

    def get_remote_host(self):
        return self.remote_host.get_remote_host()

class PrintButton(Gtk.Button):
    
    def __init__(self, parent=None):
        
        Gtk.Button.__init__(self, "Stampa")

    def set_state(self, state):
        if state is "idle":
            self.set_label ("Stampa")
        elif state is "printing":
            self.set_label ("Stampa in corso")
            # Questa è una sporca soluzione per fare in modo che
            # il cambio di stato si veda.
            while Gtk.events_pending():
                Gtk.main_iteration ()
        else:
            raise RuntimeError('Invalid state %s' % state)

class QueueButton(Gtk.Button):

    def __init__(self):
        Gtk.Button.__init__(self, "Visualizza coda")
        
    def set_state(self, state):
        if state is "idle":
            self.set_label("Visualizza coda")
        else:
            self.set_label("Recupero coda in corso...")
            while Gtk.events_pending():
                Gtk.main_iteration ()
            
        


class SelectFileWidget(Gtk.HBox):
    
    def __init__(self, filename = None):
        Gtk.HBox.__init__(self)
        self.set_spacing (5)

        self.Filename = Gtk.Entry()
        if filename is not None:
            self.Filename.set_text(filename)
            
        self.Browser = Gtk.Button("Sfoglia")

        self.Filename.set_tooltip_text("Se hai bisogno di stampare \
da un programma clicca File -> Stampa -> Stampa su file e crea un \
file .ps da selezionare qui")

        self.Browser.connect('clicked', self.SelectFile)

        self.pack_start(self.Filename, True, True, 0)
        self.pack_start(self.Browser, True, True, 0)
        self.Filename.show()
        self.Browser.show()

    def SelectFile(self, window):

	filename = self.Filename.get_text()
        
        chooser = Gtk.FileChooserDialog(
            title = "Seleziona file da stampare",
            parent = None,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK) )
        if chooser.run() == Gtk.ResponseType.OK:
            self.Filename.set_text(chooser.get_filename())


	if filename != "":
		chooser.set_filename(filename)
        
        chooser.destroy()

    def GetFile(self):
        return self.Filename.get_text()

            
class PrinterComboBox(Gtk.HBox):
    
    def __init__(self, printers = []):
        
        Gtk.HBox.__init__(self)
        self.combobox = Gtk.ComboBoxText()
        for printer in printers:
            self.combobox.append_text(printer)

        self.combobox.set_active(0)

        self.pack_start( self.combobox, True, True, 0 )
        self.combobox.show()

    def get_printer(self):
        return self.combobox.get_active_text()


class PagePerPageComboBox(Gtk.HBox):
    
    def __init__(self):
        Gtk.HBox.__init__(self)
        self.combobox = Gtk.ComboBoxText()
        self.combobox.append_text("1")
        self.combobox.append_text("2")
        self.combobox.append_text("4")

        self.combobox.set_active(0)

        self.pack_start( self.combobox, True, True, 0 )
        self.combobox.show()

    def get_page_per_page(self):
        return self.combobox.get_active_text()

class PrinterSettingsBlock(Gtk.HBox):
    
    def __init__(self, default_spacing = 5, left_padding=0, filename = None, printers = []):
         
        Gtk.HBox.__init__(self)
        
        vbox1 = Gtk.VBox(False, default_spacing)
        vbox2 = Gtk.VBox(False, default_spacing)

        self.set_spacing(default_spacing)

        label = LeftAlignedLabel("Stampante", 20)
        vbox1.pack_start(label, True, True, 0)
        label.show()

        self.printer_chooser = PrinterComboBox(printers = printers)
        vbox2.pack_start( self.printer_chooser, True, True, 0 )
        self.printer_chooser.show()

        label = LeftAlignedLabel("File", 20)
        vbox1.pack_start( label, True, True, 0 )
        label.show()

        self.select_file_widget = SelectFileWidget(filename)
        vbox2.pack_start (self.select_file_widget, True, True, 0)
        self.select_file_widget.show()

        label = LeftAlignedLabel("Pagine per foglio", 20)
        vbox1.pack_start(label,True, True, 0)
        label.show()
        
        self.page_per_page = PagePerPageComboBox()
        vbox2.pack_start(self.page_per_page, True, True, 0)
        self.page_per_page.show()

        label = LeftAlignedLabel("Numero di copie", 20)
        vbox1.pack_start(label, True, True, 0)
        label.show()

        self.copies = CopiesField()
        vbox2.pack_start(self.copies, True, True, 0)
        self.copies.show()

        self.pack_start(vbox1, True, True, 0)
        self.pack_start(vbox2, True, True, 0)

        vbox1.show()
        vbox2.show()

    def get_filename(self):
        return self.select_file_widget.GetFile()

    def get_printer(self):
        return self.printer_chooser.get_printer()

    def get_page_per_page(self):
        return self.page_per_page.get_page_per_page()

    def get_copies(self):
        return self.copies.get_copies()



class PageRangeBlock(Gtk.VBox):
    
    def __init__(self):
        
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)

        self.check_button = Gtk.CheckButton(label = "Stampa solo una parte del documento")

        self.check_button.set_active(False)

        self.check_button.connect('clicked', self.check_button_callback)

        self.pack_start(self.check_button, True, True, 0)
        self.check_button.show()

        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        self.range_field = Gtk.Entry()
        self.range_field.set_tooltip_text("Indicare pagine e/o intervalli separati da virgole, ad esempio \"1,3-10,12,13,15-17\"")

        label = LeftAlignedLabel("Range di pagine", 20)
        self.hbox.pack_start(label, True, True, 0)
        self.hbox.pack_start(self.range_field, True, True, 0)
        label.show()

        self.pack_start(self.hbox, True, True, 0)

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


class CopiesField(Gtk.SpinButton):

    def __init__(self):
        
        Gtk.SpinButton.__init__(self)
        self.set_digits(0)
        self.set_increments(1,10)
        self.set_range(0,999)
        self.set_value(1)
        
    def get_copies(self):
        return str(self.get_value())



class OrientationSelect(Gtk.HBox):
    
    def __init__(self):
        
        Gtk.HBox.__init__(self)
        
        # Un etichetta per capire a cosa servono questi radio button
        label = LeftAlignedLabel("Orientamento", 20)
        self.pack_start( label, True, True, 0 )
        label.show()
        
        # I radio button :)
        self.landscape = Gtk.RadioButton.new_with_label_from_widget (None,
                                                                     "Orizzontale")

        self.portrait  = Gtk.RadioButton.new_with_label_from_widget (self.landscape,
                                                                     "Verticale")
        self.pack_start(self.landscape, True, True, 0)
        self.pack_start(self.portrait, True, True, 0)

        self.landscape.show ()
        self.portrait.show  ()

        self.portrait.set_active(True)

    def get_orientation(self):
        
        if self.landscape.get_active():
            return "landscape"

        if self.portrait.get_active():
            return ""

        ## Questo non dovrebbe succedere
        return None

class SidesSelect(Gtk.VBox):

    def __init__(self):
        
        Gtk.VBox.__init__(self)

        self.one_sided = Gtk.RadioButton.new_with_label_from_widget (None,
                                                                     "Solo fronte")
        self.two_sided_short_edge = Gtk.RadioButton.new_with_label_from_widget (
            self.one_sided,
            "Fronte retro sul lato corto")

        self.two_sided_long_edge = Gtk.RadioButton.new_with_label_from_widget (
             self.one_sided,
             "Fronte retro sul lato lungo")

        for widget in (self.one_sided,
                       self.two_sided_short_edge,
                       self.two_sided_long_edge) :
            a = PaddingLeftWidget(widget, 20)
            self.pack_start(a, True, True, 0)
            a.show()

        self.two_sided_long_edge.set_active(True)
            
    def get_sides_select(self):
        
        if( self.one_sided.get_active() ):
            return "one-sided"

        if( self.two_sided_short_edge.get_active() ):
            return "two-sided-short-edge"

        if( self.two_sided_long_edge.get_active() ):
            return "two-sided-long-edge"

        
                                    
        
            

        
