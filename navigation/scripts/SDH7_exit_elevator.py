#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from set_goal import Navigation

from time import sleep

class WaypointPublisher():
    def __init__(self, path):
        self.done = False
        self.wp_pub = rospy.Publisher('/goal_position', Twist, queue_size=1, latch=True)
        rospy.Subscriber("/goal_position_cb", Bool, self.wp_publisher_cb)
        self.path = path
        self.wp_publisher()

    def wp_publisher(self):
        if len(self.path) > 0:
            wp = self.path.pop(0)
            print("Going to {} {} {}".format(wp.linear.x, wp.linear.y, wp.angular.z))
            self.wp_pub.publish(wp)
        else:
            self.done = True

    def wp_publisher_cb(self, msg):
        if msg.data:
            self.wp_publisher()

if __name__ == '__main__':
    rospy.init_node('waypoint_publisher')
    done_pub = rospy.Publisher('/elevator/done', Bool, queue_size=1)

    # Teleportation if using sim
    # if rospy.get_param('use_sim_time') == True:
    move = Navigation()
    
        # r = rospy.Rate(1)
        # r.sleep()
    path = []
    side = rospy.get_param('/elevator')
    if(side == "left"):
        move = Navigation()
        move.set_init_pose(pos=[53.2,6.8,0],ori=[0,0,0.999993843881,0.00350887452617],cov=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787])
        sleep(1)
        outside = Twist()
        outside.linear.x, outside.linear.y, outside.angular.z = 51.5, 6.8, 3.14159
    if(side == "right"):
        move = Navigation()
        move.set_init_pose(pos=[53.2,3.9,0],ori=[0,0,0.999993843881,0.00350887452617],cov=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787])
        sleep(1)
        outside = Twist()
        outside.linear.x, outside.linear.y, outside.angular.z = 51.5, 3.85, 3.14159
    
    #TODO: wait for callback of elevator open door
    raw_input("tell me when to exit")
    wp_pub = WaypointPublisher([outside])
    while not wp_pub.done and not rospy.is_shutdown():
        r = rospy.Rate(10)
        r.sleep()
    done_pub.publish(Bool(data=True))