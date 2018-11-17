"""
>>> from testg2c import *
>>> testg2c()
"""

lenna_loc = "lenna.png"

import cv2
import numpy as np
import GrayToColor as g2c

lenna = cv2.imread(lenna_loc)
lenna_gray = cv2.imread(lenna_loc, 0)
g2c = g2c.GrayToColor(lenna)

def showImage(image):
	cv2.imshow('image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def testg2c(*args):
	if len(args) > 3:
		return "This function does not support more than 3 arguments"
	elif len(args) == 2:
		return "This function does not support exactly 2 arguments"
	elif len(args) == 3:
		b,g,r = args
	elif len(args) == 0:
		b = "abs(sin(-x/30 + 0*pi/3))*255"
		g = "abs(sin(-x/30 + 1*pi/3))*255"
		r = "abs(sin(-x/30 + 2*pi/3))*255"
	elif len(args) == 1:
		# assuming kwargs[0] is a dictionary already
		if g2c.updateImage(args[0]):
			showImage(g2c.getProcessedImage())
		else:
			return "Invalid functions provided: ", args[0]
	else:
		return "Argument error"
	
	d = {"blue": b, "green": g, "red": r}
	if g2c.updateImage(d):
		showImage(g2c.getProcessedImage())
	else:
		return "Invalid functions provided: ", d
	