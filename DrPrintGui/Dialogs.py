import gtk, pygtk

class Dialog(gtk.Dialog):
    
    def __init__(self, title=None, buttons=None, text=None):

        gtk.Dialog.__init__(self, title,
                            None,
                            0,
                            buttons)

        

class ErrorDialog(Dialog):

    def __init__(self, error, message):
        
        Dialog.__init__(self, "Errore: %s" % error,
                        buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK)
                        )

        label = gtk.Label()
        label.set_markup(message)
        self.get_content_area().pack_start( label , False, False, 15 )
        label.show()
        
    
