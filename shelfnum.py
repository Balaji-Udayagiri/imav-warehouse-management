from text import *
	
shelf_code = None

if __name__ == '__main__':
	camera = cv2.VideoCapture(0)
	while True:
		f = open('shelf_code.txt','w')
		ret, im = camera.read()
		im, text, conf = return_text(im)
		if text != "" and text != " ":
			text.replace('_', '')
			text.replace('\\', '')
			text.replace('/', '')
			text.replace('O', '0')
			print("text detected: %s"%(text))

			to_print = 0
			rex1 = re.compile("^[0-9]{2}$")
			rex2 = re.compile("^[0-9]$")
			if rex1.match(text) or rex2.match(text):
				to_print = 1
			if(conf>60 and to_print):
				shelf_code = text
		f.write('%s\n'%shelf_code)
		f.close()

