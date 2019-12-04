#!/usr/bin/env python  
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import tf




#this method will make the robot move to the goal location
def move_to_goal(xGoal,yGoal):

   #define a client for to send goal requests to the move_base server through a SimpleActionClient
   ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

   #wait for the action server to come up
   while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
           rospy.loginfo("Waiting for the move_base action server to come up")

   goal = MoveBaseGoal()
   
   
   #set up the frame parameters
   goal.target_pose.header.frame_id = "map"
   goal.target_pose.header.stamp = rospy.Time.now()

   # moving towards the goal*/

   roll = math.radians(0)
   pitch = math.radians(0)
   yaw = math.radians(180)
   quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

   goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
   goal.target_pose.pose.orientation.x = quaternion[0]
   goal.target_pose.pose.orientation.y = quaternion[1]
   goal.target_pose.pose.orientation.z = quaternion[2]
   goal.target_pose.pose.orientation.w = quaternion[3]

   rospy.loginfo("Sending goal location ...")
   ac.send_goal(goal)

   ac.wait_for_result(rospy.Duration(600))

   if(ac.get_state() ==  GoalStatus.SUCCEEDED):
           rospy.loginfo("You have reached the destination")
           return True

   else:
           rospy.loginfo("")
           return False

if __name__ == '__main__':
   rospy.init_node('map_navigation', anonymous=False)
   x_goal = -2.02880191803
   y_goal = 4.02200937271
   print'start go to goal'
   move_to_goal(x_goal,y_goal)
   rospy.spin()
