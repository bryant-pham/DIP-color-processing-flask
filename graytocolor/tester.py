"""
usage:
$ python tester.py
or
>>> from tester import *
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

def main():
    g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"})
    showImage(g2c.getProcessedImage())

main()