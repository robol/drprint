## Some useful function to help DrPrint to
# -*- coding: utf-8 -*-

import paramiko, gobject, select, time

class PrintingError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Backend(gobject.GObject):

    def __init__(self):
        super(Backend, self).__init__()

        gobject.signal_new("auth_failed", Backend, gobject.SIGNAL_RUN_FIRST, None, ())
        gobject.signal_new('io_error', Backend, gobject.SIGNAL_RUN_FIRST, None, ())

    def send_print(self, printer, username, password, page_per_page, filename, page_range, copies, orientation, sides):
        # Get printer name
        print "Selected printer: %s" % printer
    
        # Get connection
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except:
            raise PrintingError('Impossibili inizializzare paramiko')

        try:
            client.connect('ssh.dm.unipi.it', 
                           port=22, 
                           username=username,
                           password=password)
        except paramiko.AuthenticationException, e:
            self.emit('auth_failed')
            return
        
        t = client.get_transport()
        sftp = paramiko.SFTPClient.from_transport(t)
        
        print "Printing %s" % filename

        # Questo è inevitabile.. :)
        cmd = "lpr -P%s " % printer

        # Numero di pagine
        try:
            copies = int(float(copies))
        except ValueError:
            copies = 1
        if copies is not 1:
            cmd = cmd + "-# %s " % copies


        cmd_opts = ""

        ## Pagine logiche per pagine
        if not page_per_page == 1:
            cmd_opts += "-o number-up=%s " % str(page_per_page)

        ## Da a
        if not page_range == None:
            cmd_opts += "-o page-ranges=%s " % page_range

        ## Orientazione (se è vuoto è verticale)
        if not orientation == "":
            cmd_opts += "-o %s " % orientation

        ## Long edge, short edge ed amici vari
        cmd_opts += "-o sides=%s " % sides

        ## Se ci sono opzioni dai il -o e specificale
        if not cmd_opts == "":
            cmd = cmd + "%s" % cmd_opts + " /tmp/drprint_tmp_%s" % username
       
        sftp.put(filename, "/tmp/drprint_tmp_%s" % username)

        # Aspettiamo che il trasferimento avvenga, appena trovo 
        # un metodo serio per farlo rimuovo questo time.sleep()
        time.sleep(1)

        chan = t.open_session()

        # Diamo il comando sul canale
        print "Eseguo %s" % cmd
        chan.exec_command(cmd)
        chan.close()
        exit_status = chan.recv_exit_status()

        sftp.remove("/tmp/drprint_tmp_%s" % username)

        print "Printed %s on %s (exit status = %d)" % (filename, printer, exit_status)
        if exit_status != 0:
            raise PrintingError('Il comando <b>lpr</b> non e\' andato a buon fine (Exit status = %d)' % exit_status)
