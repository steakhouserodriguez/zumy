#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:31:34 2014

@author: ajc
"""
import rospy

import geometry_msgs.msg
import sensor_msgs.msg

class ZumoCrawler:
    def __init__(self):
        self.cmd_pub=rospy.Publisher('zumy0/cmd_vel',
                                     geometry_msgs.msg.Twist,
                                     queue_size=1)
        self.msg = geometry_msgs.msg.Twist()
        self.msg.linear.x=0
        self.msg.linear.y=0
        self.msg.linear.z=0
        self.msg.angular.x=0
        self.msg.angular.y=0
        self.msg.angular.z=0

    def joy_cb(self, data):
        left=data.axes[1]
        right=data.axes[4]
        self.msg.linear.x=2*(left+right)
        self.msg.angular.z=2*(right-left)
        self.cmd_pub.publish(self.msg)

if __name__ == '__main__':
    print 'running zumy_cmd_joy.py...'
    rospy.init_node('zumy_cmd_joy')
    zc = ZumoCrawler()
    rospy.Subscriber('/joy',  sensor_msgs.msg.Joy, zc.joy_cb)
    rospy.spin()