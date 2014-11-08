#!/bin/bash
#
# This script needs to be run by /etc/rc.local on the ODROID.
#

su -l bml -c 'screen -S linux_state -d -m python /home/bml/zumy/python/linux_state_pub.py'

#su -l bml -c 'screen -S zumy_lcm_node -d -m python /home/bml/zumy/python/zumy_lcm_node.py'

screen -S zumy_lcm_node -d -m python /home/bml/zumy/python/zumy_lcm_node.py

screen -S netstarter -d -m python /home/bml/zumy/python/netstarter.py