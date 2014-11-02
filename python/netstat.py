# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 22:24:23 2014

@author: ajc
"""

import ping
import socket
import time

class NetStat:
    def __init__(self):
        self.passes=0
        self.fails=0
        
    def tick(self):
        try:
            delay= ping.do_one('192.168.1.1', 2)
            if delay is None:
                self.passes=0
                self.fails+=1
            else:
                self.passes+=1
                self.fails=0
        except socket.gaierror, e:
            print e
            self.passes = 0
            self.fails+=1
        except socket.error, e:
            print e
            self.passes=0
            self.fails+=1
        return self.passes, self.fails


if __name__=='__main__':
    ns = NetStat()
    while True:
        print ns.tick()
        time.sleep(.2)