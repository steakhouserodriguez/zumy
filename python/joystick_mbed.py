# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 11:39:03 2014

@author: ajc
"""
from mbedrpc import *
import time
import threading
import socket
import lcm
from fearing import xbox_joystick_state
from fearing import header
from fearing import carrier_state

class ZC_Carrier:
    def __init__(self, an20, a1, a2, b2, b1, id, lcm):
        self.mbed_a20=an20
        self.mbed_a1=a1
        self.mbed_a2=a2
        self.mbed_b2=b2
        self.mbed_b1=b1
        self.id=id
        self.lcm=lcm
        
        self.mblock=threading.Lock()
        
        self.health_thread=threading.Thread(target=self._health_loop)
        self.health_thread.daemon=True
        
        
    def start(self):
        self.health_thread.start()
        
    def _left_cmd(self, speed):
        if speed >= 0:
            self.mbed_a1.write(1.0-speed)
            self.mbed_a2.write(1.0)
        else:
            self.mbed_a1.write(1.0)
            self.mbed_a2.write(1.0+speed)
            
    def _right_cmd(self, speed):
        if speed >= 0:
            self.mbed_b1.write(1.0-speed)
            self.mbed_b2.write(1.0)
        else:
            self.mbed_b1.write(1.0)
            self.mbed_b2.write(1.0+speed)

    def cmd(self, l, r):
        self.mblock.acquire()
        self._left_cmd(l)
        self._right_cmd(r)
        self.mblock.release()
        
    def _health_loop(self):
        volt=0
        
        topic='{0}/carrier_state'.format(self.id)
        
        msg=carrier_state()
        msg.header=header()
        msg.header.seq=0
        
        while True:
            msg.header.seq+=1
            msg.header.time=time.time()
            
            self.mblock.acquire()
            ain=self.mbed_a20.read()*3.3            
            self.mblock.release()
            vin=ain*(4.99+15.8) / 4.99
            volt=.9*volt + .1*vin
            msg.battery_voltage=volt
            
            try:
                self.lcm.publish(topic, msg.encode())
            except IOError, e:
                print e
            time.sleep(.5)


if __name__ == '__main__':
    id=socket.gethostname()
    
    dev='/dev/ttyACM0'
    mb=SerialRPC(dev, 115200)
    
    l0=PwmOut(mb,LED1)
    l0.write(1)
    
    a1=PwmOut(mb, p21)
    a2=PwmOut(mb, p22)
    b2=PwmOut(mb, p23)
    b1=PwmOut(mb, p24)
    
    a=AnalogIn(mb, p20)
    
    lc = None
    while lc is None:
        try:
            lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        except RuntimeError as e:
            print("couldn't create LCM:" + str(e))
            time.sleep(1)
    print("LCM connected properly!")
    print("running...")
    
    zc=ZC_Carrier(a,a1,a2,b2,b1,id, lc)
    
    def handle_joy(chan, data):
        msg = xbox_joystick_state.decode(data)
        l,r = -msg.axes[1], -msg.axes[4]
        zc.cmd(l,r)
    
    zc.cmd(0,0)
    lc.subscribe('joy', handle_joy)
    zc.start()
    
    while True:
        lc.handle()
        time.sleep(.01)

