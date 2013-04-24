from gi.repository import Gtk, GObject

class Dialog(Gtk.MessageDialog):
    
    def __init__(self, buttons=Gtk.ButtonsType.NONE, mtype=Gtk.MessageType.INFO):

        Gtk.MessageDialog.__init__(self,
                                   parent = None,
                                   flags = 0,
                                   type = mtype,
                                   buttons = buttons)
                                   

class ErrorDialog(Dialog):

    def __init__(self, error, message):
        
        Dialog.__init__(self, 
                        buttons = Gtk.ButtonsType.OK,
                        mtype = Gtk.MessageType.ERROR
                        )

        self.set_markup(error)
        self.format_secondary_markup(message)

class QueueDialog(Dialog):

    def __init__(self, jobs, printer):

        Dialog.__init__(self,
                        buttons = Gtk.ButtonsType.OK,
                        mtype = Gtk.MessageType.INFO
                        )

        if len(jobs) == 0:
            self.set_markup("Non ci sono lavori in coda su <b>%s</b>." % printer)
        else:
            self.set_markup("Ci sono %d lavori in coda su <b>%s</b>:" % (len(jobs), printer))

        # Lista dei lavori
        markup = ""
        for job in jobs:
            markup += "%d) <b>%s</b> sta stampando <b>%s</b>\n" % (job['position'], job['user'],
                                                                   job['filename'])
        self.format_secondary_markup (markup)
                                 

class InfoDialog(Dialog):

    def __init__(self, error, message):
        
        Dialog.__init__(self, 
                        buttons = Gtk.ButtonsType.OK,
                        mtype = Gtk.MessageType.INFO
                        )

        self.set_markup(error)
        self.format_secondary_markup(message)

        
    
class MessageDialog(Dialog):
    
    def __init__(self, title, text):
        
        Dialog.__init__(self,
                        buttons = Gtk.ButtonsType.OK_CANCEL,
                        mtype = Gtk.MessageType.WARNING
                        )
        
        self.set_markup(title)
        self.format_secondary_markup(text)

    
class ProgressDialog(Gtk.Dialog):

    __gsignals__ = {
        'transfer-cancelled': (GObject.SIGNAL_RUN_LAST,
                               GObject.TYPE_NONE, ())
        }

    def __init__(self, filename):

        Gtk.Dialog.__init__(self, 
                            title = "Trasferimento file in corso...",
                            buttons = None)
        self.__progress_bar = Gtk.ProgressBar()
        self.__progress_bar.set_fraction(0)
        self.set_border_width(5)

        self.get_content_area().set_spacing(5)
        
        filename = filename.split("/")[-1]
        text = "Trasferimento del file %s \n sul server remoto in corso..." % filename
        label = Gtk.Label(text)
        self.get_content_area().pack_start(label, True, True, 5)
        self.get_content_area().pack_start(self.__progress_bar, True, True, 5)
        label.show()
        self.__progress_bar.show()

        cancel_button = Gtk.Button("Annulla")
        self.get_content_area().pack_start(cancel_button, True, True, 5)
        cancel_button.show()

        cancel_button.connect("clicked", self.cancel)

        self.connect("destroy", self.cancel)

    def cancel(self, widget):
        self.emit('transfer-cancelled')
        self.hide()

    def set_fraction(self, fraction):
        self.__progress_bar.set_fraction(fraction)
        while Gtk.events_pending():
            Gtk.main_iteration()

    
        
        
        
