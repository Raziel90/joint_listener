#!/usr/bin/env python
#import roslib
from TrackerListener import TrackerListener

Jointlistner=TrackerListener()
Jointlistner.joint_record(filename='recording_test.csv',path='/home/ccoppola/')
        