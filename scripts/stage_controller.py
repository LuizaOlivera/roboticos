#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import random

laser = LaserScan()
odometry = Odometry()

def odometry_callback(data):
    global odometry
    odometry = data

def laser_callback(data):
    global laser
    laser = data

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

if __name__ == "__main__":
    rospy.init_node("stage_controller_node", anonymous=False)

    rospy.Subscriber("/odom", Odometry, odometry_callback)
    rospy.Subscriber("/base_scan", LaserScan, laser_callback)

    target_x = 8.0
    target_y = 13.0
    min_distance = 0.1
    max_distance = 5.0

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    r = rospy.Rate(5)  # 5 Hz

    while not rospy.is_shutdown():
        x = odometry.pose.pose.position.x
        y = odometry.pose.pose.position.y

        distance = calculate_distance(x, y, target_x, target_y)
        angle = calculate_angle(x, y, target_x, target_y)

        if laser.ranges and min(laser.ranges) > 0.5:  # Se não houver obstáculo próximo
            rospy.loginfo("Where I am: X: %s, Y: %s", x, y)

            velocity = Twist()
            velocity.linear.x = random.uniform(0.0, 0.5)
            velocity.angular.z = random.uniform(-0.5, 0.5) 
            pub.publish(velocity)
        else:
            # Obstáculo próximo, girar no sentido oposto ao obstáculo
            rospy.loginfo("Obstacle detected. Rotating to avoid.")

            velocity = Twist()
            velocity.linear.x = 0.0
            velocity.angular.z = -1.0  # Girar no sentido oposto
            pub.publish(velocity)

        r.sleep()


