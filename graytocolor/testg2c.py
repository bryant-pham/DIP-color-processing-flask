# todo: add trackbars and make the image update automatically

"""
# make sure lenna.png is in this directory
>>> from testg2c import *
>>> showImage(lenna)
>>> showImage(lenna_gray, "lenna - grayscale")
>>> testg2c()
>>> testg2c(preset=3)  # there are 10 presets! (located in GrayToColor.py)
>>> testg2c({"blue": "255-x", "green": "255-x", "red": "255-x"})
>>> testg2c("255-x", "255-x", "255-x")  # ordered as: blue, green, red
>>> showLastChannels()
>>> interactive(4)  # uses preset 4
"""

lenna_loc = "Lenna.png"

import cv2
import numpy as np
from graytocolor import GrayToColor as g2c

lenna = cv2.imread(lenna_loc)
lenna_gray = cv2.imread(lenna_loc, 0)
g2c = g2c.GrayToColor(lenna)

def showImage(image, desc="image"):
	cv2.imshow(desc, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def showLastChannels():
	for c in ["blue", "green", "red"]:
		cv2.imshow(c, g2c.processed_channels[c])
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

# presets that don't have generators will not be interactive
def interactive(preset):
	current_preset = g2c.presets[preset]
	processed_window_name = current_preset["description"]
	ch_names = ["blue", "green", "red"]
	cv2.namedWindow(processed_window_name)
	for c in ch_names:
		cv2.namedWindow(c)

	def updateChannel(channel, func_getstr, arg_names):
		def f(i):
			d_args = dict()
			for arg_name in arg_names:
				d_args[arg_name] = cv2.getTrackbarPos(arg_name, channel)
			# def c(x,y,z): return [x,y,z]
			# c(**dict(zip(*(['z','y','x'],[1,2,3]))))
			g2c.updateImage({channel: func_getstr(**d_args)})
			cv2.imshow(processed_window_name, g2c.getProcessedImage())
			cv2.imshow(channel, g2c.processed_channels[channel])
		return f
	
	if "generator" in current_preset:
		g = current_preset["generator"]
		g_args = g["args"]
		g_f = g["generate"]
		d = dict()
		for arg_name in g_args:
			d[arg_name] = arg_name
		print("equation: " + g_f(**d))  # description
		# print("how trackbar values are used: " + g["description"]) # replaced by the line above
		for c in ch_names:
			callback = updateChannel(c, g_f, g_args)
			for k,v in g_args.items():
				cv2.createTrackbar(
					k, c, v["default_value"], v["max_value"], callback
				)
			callback(None)  # processes this channel for the first time
	else:
		g2c.updateImage(g2c.presets[preset])
	
	cv2.imshow(processed_window_name, g2c.getProcessedImage())
	for c in ch_names:
		cv2.imshow(c, g2c.processed_channels[c])
	
	while cv2.waitKey(84) < 0:  # ~ 12 fps
		pass

	cv2.destroyAllWindows()
