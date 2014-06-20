# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 00:52:28 2014

@author: ajc
"""



import lcm
import time
import datetime
import pygame

from fearing import header
from fearing import xbox_joystick_state

if __name__ == '__main__':
    lc = None
    while lc is None:
        try:
            lc = lcm.LCM('udpm://239.255.76.67:7667?ttl=1')
        except RuntimeError as e:
            print("couldn't create LCM:" + str(e))
            time.sleep(1)
    print("LCM connected properly!")
    print("running...")
    
    pygame.init()
    pygame.joystick.init()
    j=pygame.joystick.Joystick(0)
    j.init()
    print j.get_name()
    
    num_axes = j.get_numaxes()
    num_buttons = j.get_numbuttons()
    start = time.time()
    
    msg = xbox_joystick_state()
    msg.header = header()
    msg.header.seq = 0
    msg.header.time = time.time()
    while 1:
        pygame.event.pump()
        msg.header.seq+=1
        msg.header.time = time.time()
        
        msg.axes = [j.get_axis(i) for i in xrange(num_axes)]
        msg.buttons = [j.get_button(i) for i in xrange(num_buttons)]

        lc.publish('joy', msg.encode())
        time.sleep(.05)