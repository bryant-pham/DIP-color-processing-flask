import numpy as np
from math import *
import cv2
import UserFuncEval as ufe
from functools import reduce

"""
import GrayToColor as g2c
g2c = g2c.GrayToColor(lenna_img)
if g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"}):  # x is intensity of original image
    processed_image = g2c.getProcessedImage()
else:
    # there is an invalid function. check g2c.valid_functions (dict) for the specific channel
    pass
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
        
        self.processed_image = self.orig_image

        self.blue_input = "x"
        self.green_input = "x"
        self.red_input = "x"

        self.blue_ufe = ufe.UserFuncEval()
        self.green_ufe = ufe.UserFuncEval()
        self.red_ufe = ufe.UserFuncEval()

        self.valid_functions = {"blue": False, "green": False, "red": False}

        # np.vectorize(lookup_dict.get)(some_ndarray).astype(np.uint8)
        self.vec_dict_get = np.vectorize(dict.get)

    # changed_inputs holds a dictionary of a key: {"blue","green","red"}
    # and a value: {string of the function for that color}
    # example usage: g2c.updateImage({"red": "10 * x + y"})  # returns True if the function is valid
    # you can build presets using static strings
    # each color channel is processed only after a successful parse, otherwise it is left untouched and valid_functions["color"] is set to False
    def updateImage(self, changed_inputs):
        if "blue" in changed_inputs:
            self.blue_input = changed_inputs["blue"]
            if not self.blue_ufe.update(self.blue_input):
                self.valid_functions["blue"] = False
            else:
                self.blue_dict = dict(enumerate(self.blue_ufe.getOutput()))
                self.valid_functions["blue"] = True
                self.processed_blue = self.vec_dict_get(self.blue_dict, self.orig_image).astype(np.uint8)

        if "green" in changed_inputs:
            self.green_input = changed_inputs["green"]
            if not self.green_ufe.update(self.green_input):
                self.valid_functions["green"] = False
            else:
                self.green_dict = dict(enumerate(self.green_ufe.getOutput()))
                self.valid_functions["green"] = True
                self.processed_green = self.vec_dict_get(self.green_dict, self.orig_image).astype(np.uint8)

        if "red" in changed_inputs:
            self.red_input = changed_inputs["red"]
            if not self.red_ufe.update(self.red_input):
                self.valid_functions["red"] = False
            else:
                self.red_dict = dict(enumerate(self.red_ufe.getOutput()))
                self.valid_functions["red"] = True
                self.processed_red = self.vec_dict_get(self.red_dict, self.orig_image).astype(np.uint8)
        
        return reduce((lambda x,y: x or y), self.valid_functions.values())

    def getProcessedImage(self):
        return cv2.merge((self.processed_blue, self.processed_green, self.processed_red))

    

    # dict(enumerate(blue_dict))
    # dict(enumerate(green_dict))
    # dict(enumerate(red_dict))

# todo: need to normalize function values after matching them in a dictionary and before sending them out
#       (it currently performs modulo for values mapping out of the range [0, 255], and the user wouldn't be expecting that modulo in the function they wrote)
