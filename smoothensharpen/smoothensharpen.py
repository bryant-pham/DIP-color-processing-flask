"""
warning: this class may raise exceptions
usage:
>>> import smoothensharpen
>>> sns = smoothensharpen.SmoothenSharpen(some_image)
>>> sns.loadKernel("gaussian")  # choose between "gaussian", "laplacian", "uniform"
>>> sns.filter["kernel"]  # check kernel if desired. note that it is rotated 180 degrees
>>> sns.applyFilter()
>>> filtered_bgr = sns.getProcessedBGR()
>>> filtered_hls = sns.getProcessedHLS()
>>> filtered_diff = sns.getProcessedDiff()
>>> sns.loadImage(another_image)
"""

"""
todo:
    applyFilter()
        adjust normalization to impact all 3 bgr channels at the same time
"""

import numpy as np
import cv2

_ERR_GRAY_INPUT = "Grayscale image received; input image must be RGB or RGBA"

class SmoothenSharpen:
    def __init__(self, input_image):
        # images must be color
        self.bgr_image = np.zeros((1,1,3))
        if len(input_image.shape) == 3:
            if input_image.shape[2] == 3:
                self.bgr_image = input_image
            elif input_image.shape[2] == 4:
                self.bgr_image = cv2.cvtColor(input_image, cv2.COLOR_BGRA2BGR)
            else:
                raise _ERR_GRAY_INPUT
        else:
            raise _ERR_GRAY_INPUT

        # cv2 does not have a conversion to and from the HSI color space
        # so we are using HLS, and applying the filters on the L channel
        self.hls_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HLS)

        self.bgr_image_filtered = self.bgr_image.copy()
        self.hls_image_filtered = self.hls_image.copy()
        self.filtered_difference = np.full(input_image.shape, 127)
        
        self.filter = {"description": "none", "kernel": np.array([[1]]), "radius": 0}

    def loadImage(self, input_image):
        self.__init__(input_image)

    def loadKernel(self, kernel_type, radius = 1, custom_kernel = None):
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

    def applyFilter(self):
        pad_mode = "edge"  # "constant" for 0 padding, "edge" for nearest edge padding
        r = self.filter["radius"]
        d = r*2 + 1
        k = self.filter["kernel"]
        bgr_padded = np.stack([np.pad(np.split(self.bgr_image, [1,2], 2)[x][:,:,0], r, pad_mode) for x in range(3)], axis=2)
        l_padded = np.pad(np.split(self.hls_image, [1,2], 2)[1][:,:,0], r, pad_mode)

        s = self.bgr_image.shape
        for x in range(s[0]):
            for y in range(s[1]):
                for c in range(s[2]):  # color channel
                    self.bgr_image_filtered[x,y,c] = np.sum(k*bgr_padded[x:x+d,y:y+d,c])
                self.hls_image_filtered[x,y,1] = np.sum(k*l_padded[x:x+d,y:y+d])
        
        # normalize filtered images
        for c in range(s[2]):
            self.bgr_image_filtered[:,:,c] = self.normalize(self.bgr_image_filtered[:,:,c], 256).clip(0,255)
        self.hls_image_filtered[:,:,1] = self.normalize(self.hls_image_filtered[:,:,1], 256).clip(0,255)

        self.filtered_difference = np.full(s[:2], 127) \
            + cv2.cvtColor(self.bgr_image_filtered, cv2.COLOR_BGR2GRAY).astype(np.int32) \
            - self.hls_image_filtered[:,:,1]
        self.filtered_difference = self.filtered_difference.astype(np.uint8)

    # n is number of bins (256 to cover uint8)
    @classmethod
    def normalize(cls, img, n):
        # h is histogram, b is bins
        h, b = np.histogram(img.flatten(), n)
        # c is cdf
        c = h.cumsum() - 1
        c = c * (n - 1) / c[-1]
        return np.interp(img.flatten(), b[:-1], c).reshape(img.shape)

    def getProcessedBGR(self):
        return self.bgr_image_filtered
    def getProcessedHLS(self):
        return cv2.cvtColor(self.hls_image_filtered, cv2.COLOR_HLS2BGR)
    def getProcessedDiff(self):
        return self.filtered_difference
