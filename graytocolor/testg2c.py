"""
# make sure lenna.png is in this directory
>>> from testg2c import *
>>> showImage(lenna)
>>> showImage(lenna_gray, "lenna - grayscale")
>>> testg2c()
>>> testg2c(preset=3)  # there are 6 presets!
>>> testg2c({"blue": "255-x", "green": "255-x", "red": "255-x"})
>>> testg2c("255-x", "255-x", "255-x")  # order: blue, green, red
"""

lenna_loc = "lenna.png"

import cv2
import numpy as np
import GrayToColor as g2c

lenna = cv2.imread(lenna_loc)
lenna_gray = cv2.imread(lenna_loc, 0)
g2c = g2c.GrayToColor(lenna)

def showImage(image, desc="image"):
	cv2.imshow(desc, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def testg2c(*args, **kwargs):
	if "preset" in kwargs:
		if kwargs["preset"] not in g2c.presets:
			return "Valid presets: " + str(set(g2c.presets.values()))
		desc = g2c.presets[kwargs["preset"]]["description"]
		if len(desc) > 40:
			desc = desc[:37] + "..."
		g2c.updateImage(g2c.presets[kwargs["preset"]])
		showImage(g2c.getProcessedImage(), desc)
		return
	
	if len(args) > 3:
		return "This function does not support more than 3 arguments"
	elif len(args) == 2:
		return "This function does not support exactly 2 arguments"
	elif len(args) == 3:
		b,g,r = args
		d = {"blue": b, "green": g, "red": r}
		if g2c.updateImage(d):
			showImage(g2c.getProcessedImage())
			return "Functions used: " + str(d)
		else:
			return "Invalid functions provided: " + str(d)
	elif len(args) == 0:
		# show last processed image
		showImage(g2c.getProcessedImage())
		return
	elif len(args) == 1:
		# assuming kwargs[0] is a dictionary already
		if g2c.updateImage(args[0]):
			showImage(g2c.getProcessedImage())
			return
		else:
			return "Invalid functions provided"
	else:
		return "Argument error"
	return "Unknown error"
	
def scaleImage(image, scale):
	return cv2.resize(image, None, fx=scale, fy=scale)