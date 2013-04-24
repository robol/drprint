# -*- coding: utf-8 -*-
## Some useful function to help DrPrint to

import paramiko, select, time, re, os
from gi.repository import GObject

import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format = FORMAT, level = logging.INFO)

class PrintingError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Backend(GObject.GObject):

    __gsignals__ = {
        'transfer-progress': (GObject.SIGNAL_RUN_FIRST,
                             GObject.TYPE_NONE,
                             (GObject.TYPE_INT,
                             GObject.TYPE_INT)),

        'transfer-started': (GObject.SIGNAL_RUN_FIRST,
                             GObject.TYPE_NONE,
                             ()),

        'transfer-finished': (GObject.SIGNAL_RUN_FIRST,
                              GObject.TYPE_NONE,
                              ()),
        }

    def __init__(self):
        GObject.GObject.__init__(self)

    def get_queue(self, printer, remote_host, username, password):
	"""
	Obtain the queue of jobs on selected printer. It opens an SSH
	connection to the server and parse lpq -Pprinter output
	"""

        host, printer = self.split_name(printer)

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

	logging.info("Executing lpq -h %s -P%s" % (host, printer))

        stdin, stdout, stderr = client.exec_command("lpq -h %s -P%s" % (host, printer))
        output = stdout.read()

        # Parse output
        jobs = []
        for line in re.findall(r"active\s+(\w+)\s+(\d+)\s+(.+)\s+(\d+) bytes", output):
            job = {
                'position': 1,
                'user': line[0],
                'id': line[1],
                'filename': line[2],
                'size': line[3],
                }
            jobs.append (job)
        
        for line in re.findall(r"(\d)\w*\s+(\w+)\s+(\d+)\s+(.+)\s+(\d+) bytes",
                               output):
            pos = int(line[0]) + 1
            job = {
                'position': pos,
                'user': line[1],
                'id': line[2],
                'filename': line[3].strip(),
                'size': line[4]
                }
            jobs.append(job)
        return jobs
        
        
    def cancel_transfer(self, widget):
        self.__abort_transfer = True

    def split_name(self, printer):
        host = "printserver.dm.unipi.it"
        if "@" in printer:
            pos = printer.index("@")
            host = printer[pos+1:]
            printer = printer[:pos]
        else:
            printer = printer

        return host, printer

    def send_print(self, printer, username, password, page_per_page,
                   filename, page_range, copies, orientation, sides, remote_host):

        self.__abort_transfer = False
        host, printer = self.split_name(printer)

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
        
        # Questo è inevitabile.. :)
        cmd = "lpr -P%s -o position=center -o media=A4" % printer

        # Numero di pagine
        try:
            copies = int(float(copies))
        except ValueError:
            copies = 1
        if copies is not 1:
            cmd = cmd + "-# %s " % copies


        cmd_opts = " -H %s " % host

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
            self.emit('transfer-started')
            buf_size = 4096 # 4 Kb
            open_file = sftp.file("/tmp/drprint_tmp_%s" % username, "w")
            bytes_read = 0
            file_size = os.path.getsize(filename)
            with open(filename, "r") as local_handle:
                buf = None
                while(buf != ""):
                    buf = local_handle.read(buf_size)
                    bytes_read = bytes_read + len(buf)
                    if self.__abort_transfer:
                        return self.__abort_transfer
                    open_file.write(buf)
                    self.emit('transfer-progress', bytes_read, file_size)
        except OSError:
            raise PrintingError('Errore nel trasferimento del file')
        else:
            pass
        
        self.emit('transfer-finished')

        # Apriamo la sessione.
        chan = t.open_session()

        # Diamo il comando sul canale
        logging.info("Executing %s" % cmd)
        chan.exec_command(cmd)
        exit_status = chan.recv_exit_status()

        chan.close()
        if exit_status == 0:
            sftp.remove("/tmp/drprint_tmp_%s" % username)

        if exit_status != 0:
            raise PrintingError('Il comando <b>lpr</b> non e\' andato a buon fine (Exit status = %d)' % exit_status)

        return self.__abort_transfer
