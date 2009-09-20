## Some useful function to help DrPrint to
# -*- coding: utf-8 -*-

import paramiko, gobject

class Backend(gobject.GObject):

    def __init__(self):
        super(Backend, self).__init__()

        gobject.signal_new("auth_failed", Backend, gobject.SIGNAL_RUN_FIRST, None, ())

    def send_print(self, printer, username, password, page_per_page, filename, page_range):
        # Get printer name
        print "Selected printer: %s" % printer
    
        # Get connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect('ssh.dm.unipi.it', 
                           port=22, 
                           username=username,
                           password=password)
        except paramiko.AuthenticationException, e:
            self.emit('auth_failed')
            return

        channel = client.get_transport().open_session()
        
        print "Printing %s" % filename
        f = open(filename, 'r')

        # Questo è inevitabile.. :)
        cmd = "lpr -P%s " % printer

        cmd_opts = ""

        ## Pagine logiche per pagine
        if not page_per_page == 1:
            cmd_opts += "number-up=%s " % str(page_per_page)

        ## Da a
        if not page_range == None:
            cmd_opts += "page-ranges=%s" % page_range

        ## Se ci sono opzioni dai il -o e specificale
        if not cmd_opts == "":
            cmd = cmd + "-o %s" % cmd_opts
        
        ## Diamo il comando sul canale e infiliamo il file
        ## dentro lo stdin :)
        channel.exec_command(cmd)
        channel.sendall( f.read() )
        f.close()
        channel.close()

        print "Printed %s on %s" % (filename, printer)
