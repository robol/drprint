## Some useful function to help DrPrint to
# -*- coding: utf-8 -*-

import paramiko

class Backend():
    
    def __init__(self):
        pass

    def send_print(self, printer, username, password, page_per_page, filename):
        # Get printer name
        print "Selected printer: %s" % printer
    
        # Get connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect('ssh.dm.unipi.it', 
                       port=22, 
                       username=username,
                       password=password)

        channel = client.get_transport().open_session()
        
        print "Printing %s" % filename
        f = open(filename, 'r')

        # Questo è inevitabile.. :)
        cmd = "lpr -P%s " % printer

        cmd_opts = ""

        if not page_per_page == 1:
            cmd_opts += "number-up=%s " % str(page_per_page)

        if not cmd_opts == "":
            cmd = cmd + "-o %s" % cmd_opts
        
        channel.exec_command(cmd)
        channel.sendall( f.read() )
        f.close()
        channel.close()

        print "Printed %s on %s" % (filename, printer)
