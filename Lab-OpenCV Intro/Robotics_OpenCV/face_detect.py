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

class ColorTrack():
	
	def __init__(self):
		rospy.init_node('faceDetect_node',anonymous=True)
		
		self.rate = rospy.Rate(10)
		
		self.bridge = CvBridge()
		
		rospy.wait_for_message('/kinect2/qhd/image_color',Image)
		
		rospy.Subscriber('/kinect2/qhd/image_color', Image, self.image_callback, queue_size=1)
		
		self.rate.sleep()
		
	def image_callback(self,msg):
		try:
			image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		except CvBridgeError as e:
			print(e)
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
		
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray,1.3,5)
		for(x,y,w,h) in faces:
			cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = image[y:y+h, x:x+w]
			#eyes = eye_cascade.detectMultiScale(roi_gray)
			#for (ex, ey, ew, eh) in eyes:
				#cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0),2)
		cv2.imshow('img',image)
		cv2.waitKey(1)
		
		
		
	    

if __name__ == '__main__':
	try:
		colorTrack = ColorTrack()
		rospy.spin()
	except rospy.ROSInterruptException:
		rospy.loginfo("Track node terminated.")
	cv2.destroyAllWindows()
