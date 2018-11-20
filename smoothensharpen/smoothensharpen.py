"""
warning: this class may raise exceptions
usage:
>>> import smoothensharpen
>>> sns = smoothensharpen.SmoothenSharpen(some_image)
>>> sns.loadKernel("gaussian")  # choose between "gaussian", "laplacian", "uniform"
>>> sns.filter["kernel"]  # check kernel if desired. note that it is rotated 180 degrees
>>> sns.applyFilter()
>>> final_image = sns.getProcessedImage()
sns.loadImage(another_image)
"""

import numpy as np
import cv2

_ERR_GRAY_INPUT = "Grayscale image received; input image must be RGB or RGBA"

class SmoothenSharpen:
    def __init__(self, input_image):
        # images must be color
        self.bgr_image = np.zeros((1,1,3))
        if len(orig_image.shape) == 3:
            if orig_image.shape[2] == 3:
                self.bgr_image = input_image
            elif orig_image.shape[2] == 4:
                self.bgr_image = cv2.cvtColor(input_image, cv2.COLOR_BGRA2BGR)
            else:
                raise _ERR_GRAY_INPUT
        else:
            raise _ERR_GRAY_INPUT

        # cv2 does not have a conversion to and from the HSI color space
        # so we are using HLS, and applying the filters on the L channel
        self.hls_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HLS)

        self.bgr_image_filtered = np.zeros(self.bgr_image.shape)
        self.hls_image_filtered = np.zeros(self.hls_image.shape)
        self.filtered_difference = np.full(input_image.shape, 127)
        
        self.filter = {"description": "none", "kernel": np.array([[1]]), "radius": 0}
        pass

    def loadImage(self, input_image):
        self.__init__(input_image)

    def loadKernel(kernel_type, radius = 1, custom_kernel = None):
        k_length = 2*radius + 1
        kernel = np.zeros((k_length,)*2)

        if kernel_type == "gaussian" or kernel_type == "g":
            pass  # currently uses a predefined kernel
            kernel = np.array([[1,2,1],[2,8,2],[1,2,1]])
            kernel = kernel / np.sum(kernel)
        elif kernel_type == "laplacian" or kernel_type == "l":
            pass  # currently uses a predefined kernel
            kernel = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
        elif kernel_type == "uniform" or kernel_type == "u":
            kernel = (kernel + 1)
            kernel = kernel / np.sum(kernel)
            # maybe change to use a circle
        elif kernel_type == "custom" or kernel_type == "c":
            cks = custom_kernel.shape
            if len(cks) != 2:
                raise "custom kernel must be formatted as a 2D numpy array"
            if cks[0] != cks[1]:
                raise "custom kernel must have the same width and height. pad with zeros to fit requirement."
            if np.mod(cks[0], 2) == 0 or np.mod(cks[1], 2) == 0:
                raise "custom kernel may not have an even height or width"
            kernel = custom_kernel
            radius = int(len(kernel) / 2)
            s = np.sum(kernel)
            kernel = kernel if s == 0 else kernel / s
        else:
            raise "Invalid kernel type requested"

        self.filter["description"] = kernel_type
        self.filter["kernel"] = np.fliplr(np.flipud(kernel))
        self.filter["radius"] = radius

    def applyFilter():
        pad_mode = "edge"  # "constant" for 0 padding, "edge" for nearest edge padding
        r = self.filter["radius"]
        bgr_padded = np.stack([np.pad(np.split(self.bgr_image, [1,2], 2)[x][:,:,0], r, pad_mode) for x in range(3)], axis=2)
        l_padded = np.pad(np.split(self.hls_image, [1,2], 2)[1][:,:,0], r, pad_mode)

        s = self.bgr_image.shape
        for x in s[0]:
            for y in s[1]:
                # first pixel after padding is x+r, y+r
                for c in s[2]:  # color channel
                pass
                # for wx in range(-r, r+1):
                # for wy in range(-r, r+1):
        # use dot product??

        pass

    def 