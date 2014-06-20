#!/bin/bash
#
# This script needs to be run by /etc/rc.local on the ODROID.
#

su -l odroid -c 'screen -S linux_state -d -m python /home/odroid/zumocrawler/python/linux_state_pub.py'

su -l odroid -c 'screen -S joystick_mbed -d -m python /home/odroid/zumocrawler/python/joystick_mbed.py'

screen -S netstarter -d -m python /home/odroid/zumocrawler/python/netstarter.py