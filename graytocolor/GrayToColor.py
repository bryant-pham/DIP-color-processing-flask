# todo: need to normalize function values after matching them in a dictionary and before sending them out
#       (it currently performs modulo for values mapping out of the range [0, 255], and the user wouldn't be expecting that modulo in the function they wrote)
# analysis idea:
#       plot trans_dict over the domain [0,255] and compare it to a plot for intensity slicing
#       also plot the histogram of the original image with it

import numpy as np
from math import *
import cv2
import UserFuncEval as ufe
from functools import reduce

"""
import GrayToColor as g2c
g2c = g2c.GrayToColor(lenna_img)
print("Valid operations: " + str(g2c.getValidOperations()))
# x is intensity of original image:
if g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"}):
    processed_image = g2c.getProcessedImage()
else:
    # there is an invalid function. check g2c.valid_functions (dict) for the specific channel
    print("Valid functions: " + str(g2c.valid_functions))
processed_image_2 = g2c.getProcessedImage(g2c.presets[3])
g2c.loadImage(another_img)
"""

class GrayToColor:
    def __init__(self, orig_image):
        # make sure image is grayscale before processing
        if len(orig_image.shape) == 3:
            if orig_image.shape[2] == 3:
                self.orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)
            elif orig_image.shape[2] == 4:
                self.orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGRA2GRAY)
            else:
                self.orig_image = orig_image
        else:
            self.orig_image = orig_image
        
        self.processed_image = self.orig_image.copy()

        self.vec_dict_get = np.vectorize(dict.get)

        self.ufe = {
            "blue":     ufe.UserFuncEval(),
            "red":      ufe.UserFuncEval(),
            "green":    ufe.UserFuncEval(),
        }
        self.trans_dict = {"blue": dict(), "green": dict(), "red": dict()}
        self.input_strings = {"blue": "x", "green": "x", "red": "x"}
        self.valid_functions = {"blue": False, "green": False, "red": False}
        self.processed_channels = {"blue": None, "green": None, "red": None}
        self.updateImage(self.input_strings)

    def processChannel(self, channel, func_string):
        self.input_strings[channel] = func_string
        if not self.ufe[channel].update(self.input_strings[channel]):
            self.valid_functions[channel] = False
        else:
            self.trans_dict[channel] = dict(enumerate(self.ufe[channel].getOutput()))
            self.valid_functions[channel] = True
            self.processed_channels[channel] = \
                self.vec_dict_get(self.trans_dict[channel], self.orig_image).astype(np.uint8)

    # changed_inputs holds a dictionary of a key: {"blue","green","red"}
    # and a value: <string of the function for that color>
    # returns True if processing was successful, otherwise False
    # example usage: g2c.updateImage({"red": "10 * x + y"})
    # if True is returned, you may retrieve the processed image with getProcessedImage()
        # self.processed_image will not be updated until getProcessedImage() is called
        # >>> my_image = g2c.getProcessedImage()
    # else if False is returned, see which functions are invalid through printing valid_functions
        # >>> g2c.valid_functions
    # save processing time by only passing potentially changed channel inputs. eg don't pass the function for "blue" if the user hasn't changed it
    def updateImage(self, changed_inputs):
        if "blue" in changed_inputs:
            self.processChannel("blue", changed_inputs["blue"])
        if "green" in changed_inputs:
            self.processChannel("green", changed_inputs["green"])
        if "red" in changed_inputs:
            self.processChannel("red", changed_inputs["red"])
        return reduce((lambda x, y: x and y), self.valid_functions.values())

    def getProcessedImage(self):
        return cv2.merge(tuple([self.processed_channels[c] for c in ["blue", "green", "red"]]))

    def loadImage(self, image):
        self.__init__(image)

    def getValidOperations(self):
        return self.ufe["blue"].getValidOperations()

    presets = {
        1: {
            "description": "negative",
            "blue":     "255-x",
            "green":    "255-x",
            "red":      "255-x"
        },
        2: {
            "description": "purple tint",
            "blue":     "x/3+170",
            "green":    "x/3",
            "red":      "x/3+85"
        },
        3: {
            "description": "generic abs(sin(x))",
            "blue":     "abs(sin(-x/30 + 0*pi/3 - 0.2))*255",
            "green":    "abs(sin(-x/30 + 1*pi/3 - 0.2))*255",
            "red":      "abs(sin(-x/30 + 2*pi/3 - 0.2))*255"
        },
        4: {
            "description": "generic triangle wave",
            "blue":     "abs(mod(x+0,60)-30)*255/30",
            "green":    "abs(mod(x+20,60)-30)*255/30",
            "red":      "abs(mod(x+30,60)-30)*255/30"
        },
        5: {
            "description": "generic sawtooth wave",
            "blue":     "mod(x+0,60)/(60-1)*255",
            "green":    "mod(x+20,60)/(60-1)*255",
            "red":      "mod(x+40,60)/(60-1)*255"
        },
        6: {
            "description": "generic haversin wave",
            "blue":     "(1-cos(x/30+0*pi/3))/2*255",
            "green":    "(1-cos(x/30+1*pi/3))/2*255",
            "red":      "(1-cos(x/30+2*pi/3))/2*255"
        }
    }
