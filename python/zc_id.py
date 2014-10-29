# -*- coding: utf-8 -*-
"""
zc_id.py

provides an interface for robots to know their ID.
ID is stored in /home/ajc/zc_id or /home/odroid/zc_id

ID is set by
$ echo '/002' > ~/zc_id

the ID is the prefix for most channels, ie
/002/linux_state

Created on Thu Jun 19 16:57:50 2014

@author: ajc
"""

import os

def get_id():
    files='/home/ajc/zc_id', '/home/odroid/zc_id', '/home/bml/zc_id'
    for f in files:
        if os.path.exists(f):
            txt=open(f)
            id=txt.read()
            id=id.replace('\n', '')
            return id
    print "No zc_id found!"
    return None