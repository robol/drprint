## Some useful function to help DrPrint to
# -*- coding: utf-8 -*-

import paramiko, gobject

class Backend(gobject.GObject):

    def __init__(self):
        super(Backend, self).__init__()

        gobject.signal_new("auth_failed", Backend, gobject.SIGNAL_RUN_FIRST, None, ())
        gobject.signal_new('io_error', Backend, gobject.SIGNAL_RUN_FIRST, None, ())

    def send_print(self, printer, username, password, page_per_page, filename, page_range, copies, orientation, sides):
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

        try:
            f = open(filename, 'r')
        except IOError:
            self.emit('io_error')
            return

        # Questo è inevitabile.. :)
        cmd = "lpr -P%s " % printer

        # Nunmero di pagine
        if copies.isdigit():
            cmd = cmd + "-# %s " % copies


        cmd_opts = ""

        ## Pagine logiche per pagine
        if not page_per_page == 1:
            cmd_opts += "-o number-up=%s " % str(page_per_page)

        ## Da a
        if not page_range == None:
            cmd_opts += "-o page-ranges=%s" % page_range

        ## Orientazione (se è vuoto è verticale)
        if not orientation == "":
            cmd_opts += "-o %s " % orientation

        ## Long edge, short edge ed amici vari
        cmd_opts += "-o sides=%s " % sides

        ## Se ci sono opzioni dai il -o e specificale
        if not cmd_opts == "":
            cmd = cmd + "%s" % cmd_opts
       
        
        ## Diamo il comando sul canale e infiliamo il file
        ## dentro lo stdin :)
        print "Eseguo %s" % cmd

        channel.exec_command(cmd)
        try:
            content = f.read()
        except IOError:
            self.emit('io_error')
            return

        try:
            channel.sendall( content )
        except socket.timeout, socket.error:
            self.emit('io_error')
            return
        f.close()
        channel.close()

        print "Printed %s on %s" % (filename, printer)
