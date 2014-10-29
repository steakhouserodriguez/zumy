# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 06:39:30 2014

@author: ajc
"""

from mbedrpc import *
import threading

class Motor:
    def __init__(self, a1, a2):
        self.a1=a1
        self.a2=a2
    def cmd(self, speed):
        if speed >=0:
            self.a1.write(speed)
            self.a2.write(0)
        else:
            self.a1.write(0)
            self.a2.write(-speed)

class Zumy:
    def __init__(self, dev='/dev/ttyACM0'):
        self.mbed=SerialRPC(dev, 115200)
        a1=PwmOut(self.mbed, p21)
        a2=PwmOut(self.mbed, p22)
        b1=PwmOut(self.mbed, p23)
        b2=PwmOut(self.mbed, p24)
        self.m_right = Motor(a1, a2)
        self.m_left = Motor(b1, b2)
        self.an = AnalogIn(self.mbed, p20)
        self.rlock=threading.Lock()

#    def enable(self):
#        self.rlock.acquire()
#        self.enabled=True
#        self._cmd(self.last_left, self.last_right)
#        self.rlock.release()
#
#    def disable(self):
#        self.rlock.acquire()
#        self.enabled=False
#        self._cmd(self.last_left, self.last_right)
#        self.rlock.release()

#    def drive(self, left, right):
#        self._cmd(left, right)
#
#    def cmd(self, left, right):
#        self._cmd(left, right)

    def cmd(self, left, right):
#        self.last_left=left
#        self.last_right=right
#        if self.enabled:
        self.rlock.acquire()
        self.m_left.cmd(-left)
        self.m_right.cmd(right)
        self.rlock.release()
#        else:
#            self.m_left.cmd(0)
#            self.m_right.cmd(0)

    def read_voltage(self):
        self.rlock.acquire()
        ain=self.an.read()*3.3 
        self.rlock.release()
        volt=ain*(4.99+15.8) / 4.99
        return volt
        
#        def read(sensor): return sensor.read()
#        retu=map(read, self.sensors)
#        return retu
        
if __name__ == '__main__':
    z=Zumy('/dev/ttyACM1')
    