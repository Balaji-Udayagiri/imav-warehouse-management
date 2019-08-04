from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import sys
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
	sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import re
from djitellopy import Tello
import imutils as imu
from time import sleep     
import os
import random
import time
import asyncio
import numpy as np
import cv2
import pytesseract
from qrcode import *
from text import *

<<<<<<< HEAD
Mat src, srcHSV;
Mat srcH;
vector<Mat> channels;
=======
def apply_contrast(im):
	lab= cv2.cvtColor(im, cv2.COLOR_BGR2LAB)

	#-----Splitting the LAB image to different channels-------------------------
	l, a, b = cv2.split(lab)

	#-----Applying CLAHE to L-channel-------------------------------------------
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl = clahe.apply(l)

	#-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
	limg = cv2.merge((cl,a,b))

	#-----Converting image from LAB Color model to RGB model--------------------
	im = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

	return im

def apply_thresh(img):

	img1 = np.zeros(img.shape)
	mask = np.multiply(np.multiply((img[:][:][0]<100), (img[:][:][1]<100)), (img[:][:][2]<100))
	mask = np.invert(mask)
	for channel in range(3):
		img1[:][:][channel] = np.multiply(mask, img[:][:][channel])
	return img1 
>>>>>>> 5110b4b916799b1e679d5dc031cc1fd7e36851c5

tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()
rcout = np.zeros(4)

def img_resize(im):
	fx = 7.092159469231584126e+02
	fy = 7.102890453175559742e+02
	cx = 3.681653710406367850e+02
	cy = 2.497677007139825491e+02

	"""fx = 672.074266
	fy = 672.019640
	cx = 324.846853
	cy = 255.070573"""

	depth = 200
	real_text_w = 150	#200
	real_text_h = 60	#100
	favg = (fx+fy)/2
	text_w = (real_text_w*favg)/depth
	text_h = (real_text_h*favg)/depth

	optical_text_w = 172
	optimal_text_h = 74
	k = optimal_text_h/text_h
	rows = int(im.shape[0] * 1.2)
	cols = int(im.shape[1] * 1.2)
	dim = (cols, rows)
	resized = cv2.resize(im, dim, interpolation = cv2.INTER_LINEAR)
	return resized

# Main 
if __name__ == '__main__':
 
	f = open('warehouse.csv','w')
	f.write('%s,%s,\n'%("QR_Data", "Alphanum_text"))
	f.close()

	# Read feed
	#camera = cv2.VideoCapture(0)
	#capture = tello.get_video_capture()
	frame_read = tello.get_frame_read()

	while True:
		#ret, im = camera.read()
		
		frameBGR = np.copy(frame_read.frame)
		im = imu.resize(frameBGR, width=720)
		
		im_hsv = (im, cv2.COLOR_BGR2HSV);
		cv2.split(im, channels);
		
		
		im, qrpoints, qrlist = main(im)
		if qrpoints != []:
	  		print(qrlist)

		#RESIZE
		#CROP
		im = img_resize(im)
		im = apply_contrast(im)
		im, text, conf = return_text(im)
		print(len(qrlist))
		for i in range(len(qrlist)):
			Data = qrlist[i]
			
			#Print recognized text
			if text != "" and text != " ":
				text = text.replace('_', '')
				text = text.replace('\\', '')
				text = text.replace('/', '')
				text = text.replace('O', '0')
				print("text detected: %s"%(text))

				to_print = 0
				rex1 = re.compile("^[0-9]{2}[A-Z]$")
				rex2 = re.compile("^[0-9][A-Z]$")
				if rex1.match(text) or rex2.match(text):
					to_print = 1

				if(conf>60 and to_print):
					print()
					print()
					print("YAYAYAYAYAYYYY")
					print()
					print()
					f = open('warehouse.csv','a')
					f.write('%s,%s,\n'%(Data, text))
					f.close()

		cv2.imshow("Results", im)
		key = cv2.waitKey(1) & 0xFF;
		if key == ord("t"):
			tello.takeoff()    
		elif key == ord("l"):
			tello.land()
		elif key == ord("w"):
			rcOut[1] = 25
		elif key == ord("a"):
			rcOut[0] = -25
		elif key == ord("s"):
			rcOut[1] = -25
		elif key == ord("d"):
			rcOut[0] = 25
		elif key == ord("u"):
			rcOut[2] = 25
		elif key == ord("j"):
			rcOut[2] = -25
		elif key == ord("q"):
			breaks
		else:
			rcOut = [0,0,0,0]

		# print self.rcOut
		tello.send_rc_control(int(rcOut[0]),int(rcOut[1]),int(rcOut[2]),int(rcOut[3]))
		rcOut = [0,0,0,0]

	f.close()

tello.end()
#capture.release()
cv2.destroyAllWindows()
tello.streamoff()





	  
