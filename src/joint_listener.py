#!/usr/bin/env python
#import roslib
import rospy
import tf

rospy.init_node('kinect_listener', anonymous=True)
'''BASE_FRAME="/openni_depth_frame"'''
BASE_FRAME="/tracker_depth_frame"
FRAMES=[
        'head',
        'neck',
        'torso',
        'left_shoulder',
        'left_elbow',
        'left_hand',
        'left_hip',
        'left_knee',
        'left_foot',
        'right_shoulder',
        'right_elbow',
        'right_hand',
        'right_hip',
        'right_knee',
        'right_foot',
        ]
        
LAST = rospy.Duration()        
n_user="1"
user='/tracker/user_'+n_user
#creation of a Trasform Listener node
listener=tf.TransformListener()
while not rospy.is_shutdown():
    try:
        frames=[]
        for frame in FRAMES:
            #listener.waitForTransform(BASE_FRAME, "/left_knee_1", LAST, rospy.Duration(4.0))
            #print BASE_FRAME
            (trans,rot) = listener.lookupTransform(BASE_FRAME, user+'/'+frame, LAST)
            #print trans
            frames.append((frame,trans,rot))
        print frames
    except(tf.LookupException,
           tf.ConnectivityException,
           tf.ExtrapolationException) as ex:
               print ex
               continue
   