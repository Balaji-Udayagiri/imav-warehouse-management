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


tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()

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
	rows = int(im.shape[0] * k)
	cols = int(im.shape[1] * k)
	dim = (cols, rows)
	resized = cv2.resize(im, dim, interpolation = cv2.INTER_LINEAR)
	return resized

# Main 
if __name__ == '__main__':
 
	f = open('warehouse.csv','w')
	f.write('%s,%s,\n'%("QR_Data", "Alphanum_text"))

	# Read feed
	#camera = cv2.VideoCapture(0)
	#capture = tello.get_video_capture()
	frame_read = tello.get_frame_read()
	while True:
		#ret, im = camera.read()
		
		frameBGR = np.copy(frame_read.frame)
		im = imu.resize(frameBGR, width=720)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		im, qrpoints, qrlist = main(im)
		if qrpoints != []:
	  		print(qrlist)

		#RESIZE
		#CROP
		im = img_resize(im)
		im, text, conf = return_text(im)
		print(len(qrlist))
		for i in range(len(qrlist)):
			Data = qrlist[i]
			
			#Print recognized text
			if text != "" and text != " ":
				text.replace('_', '')
				text.replace('\\', '')
				text.replace('/', '')
				text.replace('O', '0')
				print("text detected: %s"%(text))

				to_print = 0
				rex1 = re.compile("^[0-9]{2}[A-Z]$")
				rex2 = re.compile("^[0-9][A-Z]$")
				if rex1.match(text) or rex2.match(text):
					to_print = 1

				if(conf>60 and to_print):
					f.write('%s,%s,\n'%(Data, text))

		cv2.imshow("Results", im)
		cv2.waitKey(1)

	f.close()

tello.end()
capture.release()
cv2.destroyAllWindows()
tello.streamoff()





	  
