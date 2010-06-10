## Some useful function to help DrPrint to
# -*- coding: utf-8 -*-

import paramiko, gobject, select, time, re

class PrintingError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Backend(gobject.GObject):

    def __init__(self):
        super(Backend, self).__init__()

    def get_queue(self, printer, remote_host, username, password):

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except:
           raise RuntimeError('Impossibile inizializzare paramiko')
        
        try:
            client.connect(remote_host,
                           port = 22,
                           username = username,
                           password = password)
        except:
            raise RuntimeError('Impossibile connettersi a %s' % remote_host)

        stdin, stdout, stderr = client.exec_command("lpq -P%s" % printer)
        output = stdout.read()

        # Parse output
        jobs = []
        for line in re.findall(r"(\d+)\w*\s+(\w+)\s+(\d+)\s+(.+)\s+(\d+) bytes",
                               output):
            job = {
                'position': int(line[0]),
                'user': line[1],
                'id': line[2],
                'filename': line[3].strip(),
                'size': line[4]
                }
            jobs.append(job)
        return jobs
        
        


    def send_print(self, printer, username, password, page_per_page,
                   filename, page_range, copies, orientation, sides, remote_host):
        
        # Get printer name
        print "Selected printer: %s" % printer
    
        # Get connection
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except:
            raise PrintingError('Impossibili inizializzare paramiko')

        try:
            client.connect(remote_host, 
                           port=22, 
                           username=username,
                           password=password)
        except paramiko.AuthenticationException, e:
            raise PrintingError('Autenticazione fallita')
        except Exception, e:
            raise PrintingError('Connessione fallita (%s)' % e)
        
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

        try:
            attr = sftp.put(filename, "/tmp/drprint_tmp_%s" % username)
        except OSError:
            raise PrintingError('Errore nel trasferimento del file')
        else:
            print "File trasferito, dimensione: %d bytes" % attr.st_size

        # Apriamo la sessione.
        chan = t.open_session()

        # Diamo il comando sul canale
        print "Eseguo %s" % cmd
        chan.exec_command(cmd)

        exit_status = chan.recv_exit_status()
        chan.close()
        if exit_status == 0:
            sftp.remove("/tmp/drprint_tmp_%s" % username)

        print "Printed %s on %s (exit status = %d)" % (filename, printer, exit_status)
        if exit_status != 0:
            raise PrintingError('Il comando <b>lpr</b> non e\' andato a buon fine (Exit status = %d)' % exit_status)
