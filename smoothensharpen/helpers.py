# >>> from helpers import *

import cv2
import smoothensharpen as sns

def showImage(image):
	cv2.imshow('image', image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
def showImages(images):
	n = 1
	for x in images:
		cv2.imshow(str(n), x)
		n += 1
	cv2.waitKey(0)
	cv2.destroyAllWindows()



lenna = cv2.imread("lenna.png")
sns = sns.SmoothenSharpen(lenna)
sns.loadKernel("gaussian")
sns.applyFilter()
sns.showImage(sns.getProcessedBGR())
sns.showImage(sns.getProcessedHLS())
sns.showImage(sns.getProcessedDiff())

