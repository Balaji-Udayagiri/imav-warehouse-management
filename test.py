import cv2
camera = cv2.VideoCapture(0)
while False:
	ret, im = camera.read()
	cv2.imshow("win", im)
	key = cv2.waitKey(1) & 0xFF;
	if key == ord("a"):
		print("key found")
	else:
		pass
	#cv2.destroyAllWindows()

text = "FDOOOfsd"
text = text.replace("O", "0")
print(text)