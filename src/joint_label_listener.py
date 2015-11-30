#!/usr/bin/env python
#import roslib
import rospy
import tf
import time

def get_joint_info(listener,user):
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
            
    LAST = rospy.Duration(0.1)        
    user="/tracker/user_"+str(user)
    

    try:
        frames=[]
        now=rospy.Time.now()
        for frame in FRAMES:
            listener.waitForTransform(BASE_FRAME, frame+user,now, rospy.Duration(4.0))
            #currenttime=listener.getLatestCommonTime(BASE_FRAME, frame+user)
            
            (trans,rot) = listener.lookupTransform(BASE_FRAME,  user+'/'+frame, now)
                #print trans
                #print lasttime-listener.getLatestCommonTime(BASE_FRAME, frame+user)
            frames.append((frame,trans,rot))
        #listener.clear()
        #lasttime=listener.getLatestCommonTime(BASE_FRAME, frame+user)
        return frames 
    except(tf.LookupException,
           tf.ConnectivityException,
           tf.ExtrapolationException) :
               pass
                       

    
                         
                       
if __name__ == '__main__':
    
    rospy.init_node('kinect_listener', anonymous=True)
    #creation of a Trasform Listener node
    listener=tf.TransformListener()
    f=open('some.csv', 'w')
    #writer=csv.writer(f,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    firstrow='head,,,,,,,neck,,,,,,,torso,,,,,,,left_shoulder,,,,,,,left_elbow,,,,,,,left_hand,,,,,,,left_hip,,,,,,,left_knee,,,,,,,left_foot,,,,,,,right_shoulder,,,,,,,right_elbow,,,,,,,right_hand,,,,,,,right_hip,,,,,,,right_knee,,,,,,,right_foot\n'
    coordinates=['x','y','z','a','b','c','d']
    f.writelines(firstrow)    
    for i in range(15):
        f.writelines(coordinates[0]+','+coordinates[1]+','+coordinates[2]+','+coordinates[3]+','+coordinates[4]+','+coordinates[5]+','+coordinates[6]+',')
    f.writelines('\n')
        
    
    listener.waitForTransform('/openni_depth_frame', 'head_1',rospy.Time(), rospy.Duration(4.0))
    t0=time.clock()    
    while not rospy.is_shutdown():
        try:
            full_body_joints=get_joint_info(listener,1)
            if full_body_joints is not None:
                print time.clock()-t0,'s'
                
                """for k in range(3)[1:]:
                    for j in range(len(full_body_joints[0][k])):
                        coordinates=[('x','y','z'),('a','b','c','d')]
                        f.writelines(coordinates[k-1][j]+',')
                        for i in range(len(full_body_joints)):
                            f.writelines(str(full_body_joints[i][k][j])+',')
                            #print j,i,full_body_joints[i][j]
                        f.writelines('\n')                
                    
                f.writelines('\n')
                """
                
                for joint in full_body_joints:
                    f.writelines(str(joint[1][0])+','+str(joint[1][1])+','+str(joint[1][2])+','+str(joint[2][0])+','+str(joint[2][1])+','+str(joint[2][2])+','+str(joint[2][3])+',')
                f.writelines('\n')
                #writer.writerows(unicode([full_body_joints[0][0]]))#,full_body_joints[0][1],full_body_joints[0][2])
            else:
                t0=time.clock()
        except(tf.LookupException,
           tf.ConnectivityException,
           tf.ExtrapolationException) as ex:
               print ex
               continue
         