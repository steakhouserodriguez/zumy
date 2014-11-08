# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 17:01:16 2014

@author: ajc
"""
import time
import threading
import psutil
import lcm
import socket
from fearing import header
from fearing import linux_state

import os
def get_temp():
    files=('/sys/devices/virtual/thermal/thermal_zone0/temp')
    if os.path.exists(files):
        txt=open(files)
        id=txt.read()
        id=id.replace('\n', '')
        return int(id)/1000

class LinuxStatePub:
    def __init__(self, id, lcm):
        self.id=id
        self.lcm=lcm

        self.health_thread=threading.Thread(target=self._health_loop)
        self.health_thread.daemon=True

    def start(self):
        self.health_thread.start()
        
    def _health_loop(self):
        topic='{0}/linux_state'.format(self.id)
        
        msg=linux_state()
        msg.header=header()
        msg.header.seq=0
        
        while True:
            msg.header.seq+=1
            msg.header.time=time.time()
            
            msg.temp=get_temp()
            
            cpu_perc=[0,0,0,0]
            cpu_percent=psutil.cpu_percent(percpu=True)
            for i in range(len(cpu_percent)):
                cpu_perc[i] = cpu_percent[i]
                
                
            msg.cpu_use=cpu_perc
            msg.load_average=os.getloadavg()
            
            msg.uptime=time.time()-psutil.boot_time()
            msg.memory_use=psutil.virtual_memory().used/(1024*1024)

            try:
                self.lcm.publish(topic, msg.encode())
            except IOError, e:
                print e
            time.sleep(.5)


if __name__=='__main__':
    id=socket.gethostname()
    lc = None
    while lc is None:
        try:
            lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        except RuntimeError as e:
            print("couldn't create LCM:" + str(e))
            time.sleep(1)
    print("LCM connected properly!")
    print("running...")
    lhp=LinuxStatePub(id, lc)
    lhp.start()
    
    while True:
        lc.handle()
        time.sleep(.01)
