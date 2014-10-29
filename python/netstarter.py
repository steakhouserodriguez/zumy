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
import netifaces

def reset_networking(ifaces):
    for iface in ifaces:
        proc=subprocess.Popen(['ifdown', iface])
        proc.wait()
        proc2=subprocess.Popen(['ifup', iface])
        proc2.wait()


def get_wlans():
    ifs=netifaces.interfaces()
    retu=[]
    for i in ifs:
        if i[0] is 'w':
            retu.append(i) 
    return retu

if __name__=='__main__':
    consecutive_problems=0
    while True:
        try:
            delay= ping.do_one('192.168.1.1', 2)
            if delay is None:
                print 'delay is none...'
                consecutive_problems+=1
                if consecutive_problems > 10:
                    reset_networking(get_wlans())
                    consecutive_problems=0
            else:
                print 'delay to 192.168.1.1={0} ms'.format(delay*1000)
                consecutive_problems=0
        except socket.gaierror, e:
            print e
            consecutive_problems+=1
            if consecutive_problems > 10:
                reset_networking(get_wlans())
                consecutive_problems=0
        except socket.error, e:
            print e
            consecutive_problems+=1
            if consecutive_problems > 10:
                reset_networking(get_wlans())
                consecutive_problems=0
        time.sleep(.2)