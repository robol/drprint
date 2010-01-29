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

    
