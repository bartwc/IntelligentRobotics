#!/usr/bin/env python
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy
import tf
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
import numpy as np
from matplotlib import pyplot as plt
import time

class ColorTrack():
	
	def __init__(self):
		rospy.init_node('hist_node',anonymous=True)
		
		self.rate = rospy.Rate(0.2)
		
		self.bridge = CvBridge()
		
		rospy.wait_for_message('/kinect2/qhd/image_color',Image)
		
		rospy.Subscriber('/kinect2/qhd/image_color', Image, self.image_callback, queue_size=1)
		
		self.rate.sleep()
		
	def image_callback(self,msg):
		try:
			image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		except CvBridgeError as e:
			print(e)
		
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                equ=cv2.equalizeHist(gray)
		cv2.imshow('gray',gray)
                cv2.imshow('equ',equ)
                cv2.waitKey(1)
                #cv2.imshow('image',equ)
		#cv2.waitKey(1)
               
		
		
		
	    

if __name__ == '__main__':
	try:
		colorTrack = ColorTrack()
		rospy.spin()
	except rospy.ROSInterruptException:
		rospy.loginfo("Track node terminated.")
	cv2.destroyAllWindows()
