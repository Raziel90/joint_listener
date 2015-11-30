#!/usr/bin/env python
#import roslib
import rospy
import tf
import curses












class TrackerListener:
    #here the class got inizialized: 
        """it requires:
           the name of the node to be created
           the number of the user to be tracked
           the base frame for collecting the trasformation points
           the frames relative to the base frame
           all of this arguments have default values so that it can be used without setting parameters
        """
        def __init__(self,name='body_joint_listener',user=1,BASE_FRAME = '/tracker_depth_frame',FRAMES = [
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
                                                                                                    'right_foot']
                                                                                                    ):

         rospy.init_node(name,anonymous='True')
         self.listener=tf.TransformListener()
         self.user="/tracker/user_"+str(user)
         self.BASE_FRAME=BASE_FRAME
         self.FRAMES=FRAMES        
         print 'waiting for joint points of user '+str(user)+'...'
         self.listener.waitForTransform(BASE_FRAME, self.user+'/'+self.FRAMES[0],rospy.Time(), rospy.Duration(4.0))

        
        def get_joint_info(self):
        
            try:
                frames=[]
                now=rospy.Time.now()
                for frame in self.FRAMES:
                    
                    self.listener.waitForTransform(self.BASE_FRAME, self.user+'/'+frame,now, rospy.Duration(4.0))
                    #currenttime=listener.getLatestCommonTime(BASE_FRAME, frame+user)
                    
                    (trans,rot) = self.listener.lookupTransform(self.BASE_FRAME, self.user+'/'+frame, now)
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
                       
        def joint_echo(self):
            while not rospy.is_shutdown():
                try:
                    full_body_joints=self.get_joint_info()
                    if full_body_joints is not None:
                        print full_body_joints
                except(tf.LookupException,
                       tf.ConnectivityException,
                       tf.ExtrapolationException) as ex:
                           print ex
                           continue
                       
        def joint_record(self,filename='joint_recording.csv',path='./'):
            f=open(path+filename, 'w')
            #writer=csv.writer(f,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            firstrow='head,,,,,,,neck,,,,,,,torso,,,,,,,left_shoulder,,,,,,,left_elbow,,,,,,,left_hand,,,,,,,left_hip,,,,,,,left_knee,,,,,,,left_foot,,,,,,,right_shoulder,,,,,,,right_elbow,,,,,,,right_hand,,,,,,,right_hip,,,,,,,right_knee,,,,,,,right_foot\n'
            coordinates=['x','y','z','a','b','c','d']
            f.writelines(firstrow)    
            for i in range(15):
                f.writelines(coordinates[0]+','+coordinates[1]+','+coordinates[2]+','+coordinates[3]+','+coordinates[4]+','+coordinates[5]+','+coordinates[6]+',')
            f.writelines('\n')
            screen=curses.initscr()
            t0=rospy.Time.now()
            counter=0
            while not rospy.is_shutdown():
                try:
                    full_body_joints=self.get_joint_info()
                    if full_body_joints is not None:
                        screen.clear()
                        curses.endwin()
                        currenttime=(rospy.Time.now() - t0)
                        counter=counter+1
                        print 'time elapsed',str(float(currenttime.secs)+float(currenttime.nsecs)/pow(10,9)) +' s','\nnumber of samples:',counter
                        
                        for joint in full_body_joints:
                            f.writelines(str(joint[1][0])+','+str(joint[1][1])+','+str(joint[1][2])+','+str(joint[2][0])+','+str(joint[2][1])+','+str(joint[2][2])+','+str(joint[2][3])+',')
                        f.writelines('\n')
                    else:
                        t0=rospy.Time.now()
                except(tf.LookupException,
                   tf.ConnectivityException,
                   tf.ExtrapolationException) as ex:
                       print ex
                       continue