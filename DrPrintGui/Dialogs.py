import gtk, pygtk

class Dialog(gtk.MessageDialog):
    
    def __init__(self, buttons=gtk.BUTTONS_NONE, mtype=gtk.MESSAGE_INFO):

        gtk.MessageDialog.__init__(self,
                                   parent = None,
                                   flags = 0,
                                   type = mtype,
                                   buttons = buttons)
                                   

class ErrorDialog(Dialog):

    def __init__(self, error, message):
        
        Dialog.__init__(self, 
                        buttons = gtk.BUTTONS_OK,
                        mtype = gtk.MESSAGE_ERROR
                        )

        self.set_markup(error)
        self.format_secondary_markup(message)

class QueueDialog(Dialog):

    def __init__(self, jobs, printer):

        Dialog.__init__(self,
                        buttons = gtk.BUTTONS_OK,
                        mtype = gtk.MESSAGE_INFO
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
                        buttons = gtk.BUTTONS_OK,
                        mtype = gtk.MESSAGE_INFO
                        )

        self.set_markup(error)
        self.format_secondary_markup(message)

        
    
class MessageDialog(Dialog):
    
    def __init__(self, title, text):
        
        Dialog.__init__(self,
                        buttons = gtk.BUTTONS_OK_CANCEL,
                        mtype = gtk.MESSAGE_WARNING
                        )
        
        self.set_markup(title)
        self.format_secondary_markup(text)

    
