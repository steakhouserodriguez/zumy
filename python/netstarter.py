# -*- coding: utf-8 -*-
"""
netstarter.py

restarts the network in the event of any failure to talk to 
ping the access point.

Created on Thu Jun 19 18:04:56 2014

@author: ajc
"""
import time
import ping
import socket
import subprocess

def reset_networking():
    proc=subprocess.Popen(['/etc/init.d/networking', 'restart'])
    proc.wait()

if __name__=='__main__':
    consecutive_problems=0
    while True:
        try:
            delay= ping.do_one('192.168.1.1', 2)
            if delay is None:
                print 'delay is none...'
                consecutive_problems+=1
                if consecutive_problems > 10:
                    reset_networking()
                    consecutive_problems=0
                #reset_networking()
            else:
                print 'delay to 192.168.1.1={0} ms'.format(delay*1000)
                consecutive_problems=0
        except socket.gaierror, e:
            print e
            reset_networking()
        except socket.error, e:
            print e
            reset_networking()
        time.sleep(.2)