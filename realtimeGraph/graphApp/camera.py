
from imutils.video import VideoStream
import cv2,os,urllib.request
import numpy as np
class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()
