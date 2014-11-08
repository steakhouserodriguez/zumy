# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 22:41:09 2014

@author: ajc
"""

import netstat
import time
import lcm
import threading

class LCM_Refresher:
    
    def __init__(self):
        self._ns = netstat.NetStat()
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon=True
        
    def start(self):
        self._thread.start()
        
    def _loop(self):
        while True:
            passes, fails =  self._ns.tick()
            # print passes, fails
            if passes < 50 and passes % 10 is 0:
                # print 'refreshing lcm...'
                try:
                    lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
                except RuntimeError as e:
                    print("couldn't create LCM:" + str(e))
            time.sleep(.2)

if __name__=='__main__':
    lcr=LCM_Refresher()
    lcr.start()
    while True:
        time.sleep(.2)