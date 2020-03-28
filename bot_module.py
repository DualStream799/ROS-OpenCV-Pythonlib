#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "DualStream799"

# Importing ROS related Libraries:
import rospy
from geometry_msgs.msg import Twist, Vector3  #
from sensor_msgs.msg import LaserScan               # "/scan" reciever
from std_msgs.msg import UInt8                      # "/bumper" reciever
from sensor_msgs.msg import Image, CompressedImage  # "/kamera" reciever

# Importing Computer Vision related Libraries:
from cv_bridge import CvBridge, CvBridgeError
import cv2

# Importing Support related Libraries:
import numpy as np
import math
import time

class TurtleBot():
    """docstring for TurtleBot"""

    def __init__(self):

        self.cv_bridge = CvBridge()


        # Recieves the "/scan" Subscriber data:
        self.scan_data = []
        # Recieves the "/bumper" Subscriber data:
        self.bumper = 0
        # Recieves the "scan_data" element corresponding with frontal distance:
        self.ahead = 1.0
        # Standard speed for insert on "Vector3" objects:
        self.linear_x = 0
        self.linear_y = 0
        self.linear_z = 0
        self.angular_x = 0
        self.angular_y = 0
        self.angular_z = 0
        # Basic vectors for simple bot maneuvers:
        self.vector_zero = Vector3(0, 0, 0)
        self.vector_forward = Vector3(self.linear_x, 0, 0)
        self.vector_backwards = Vector3(-self.linear_x, 0, 0)
        self.vector_turn_left = Vector3(0, 0, self.angular_z)
        self.vector_turn_right = Vector3(0, 0, -self.angular_z)

    # METHODS FOR COMPUTER VISION PROCESSMENTS:
    def frame_flip(frame, flip_mode):
        """Recieves a webcam frame and flips it or not, depending on 'flip' argument
        'flip_mode' = 0 : X-axis Flip (Vertical)
        'flip_mode' > 0 : Y-axis Flip (Horizontal)
        'flip_mode' < 0 : Both-axis Flip(Vertical and Horizontal)"""
        return cv2.flip(frame, flip_mode)


    def frame_spacecolors(frame):
        """Recieves a frame and returns frames on different spacecolors (and flipped)"""
        # Original frame (OpenCV's default frames are BGR):
        bgr_frame = frame
        # Converts frame from BGR to Grayscale:
        gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        # Converts frame from BGR to RGB:
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        # Converts frame from RGB to HSV:
        hsv_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2HSV)
        
        return bgr_frame, gray_frame, rgb_frame, hsv_frame


    def frame_capture(self, filename, frame):
        """Saves a frame on a .jpg file"""
        cv2.imwrite(filename + '.jpg', frame)


    # METHODS FOR DISPLAY CONFIGURATIONS:
    def display_aim(self, rgb_frame, point, color, width, length):
        """Draws a '+' over a given point"""
        cv2.line(rgb_frame, (point[0] - length/2, point[1]), (point[0] + length/2, point[1]), color, width, length)
        cv2.line(rgb_frame, (point[0], point[1] - length/2), (point[0], point[1] + length/2), color, width, length) 
    

    # METHODS FOR DEALING WITH ROS DATA SENSORS OR ITS MOVIMENTATION:
    def laser_scan(self, data):
        """Deals with "/scan" Subscriber data"""
        self.scan_data = np.array(data.ranges).round(decimals=2)
        self.ahead = self.scan_data[0]

    def bumper_scan(self, dado):
        """Deals with "/bumper" Subscriber data"""
        self.bumper = dado.data

    def convert_compressed_to_cv2(self, image):
        """Deals with '/kamera' Subscriber data"""
        return self.cv_bridge.compressed_imgmsg_to_cv2(image, "bgr8")
    def run_bot(self, execute_method):
        """Executes an algorithm based on the available ones"""
        if __name__ == "__main__":
            rospy.init_node("bot_module")
            try:
                while not rospy.is_shutdown():
                    if self.change_key == False:
                        execute_method()
                    else:
                        select_mode = 0

            except rospy.ROSInterruptException:
                print("Ocorreu uma exceção com o rospy")
