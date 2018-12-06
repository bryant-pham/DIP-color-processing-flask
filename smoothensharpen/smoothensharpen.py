"""
warning: this class may raise exceptions
usage:
>>> from smoothensharpen import smoothenSharpen as sns
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
import math
from scipy.ndimage import gaussian_filter, laplace

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
        self.hls_image = cv2.cvtColor(self.bgr_image, cv2.COLOR_BGR2HSV)

        self.bgr_image_filtered = self.bgr_image.copy()
        self.hls_image_filtered = self.hls_image.copy()
        self.filtered_difference = np.full(input_image.shape, 127)
        
        self.filter = {"description": "none", "kernel": np.array([[1]]), "radius": 0}

    def loadImage(self, input_image):
        self.__init__(input_image)

    def loadKernel(self, kernel_type, kernel_args):
        kernel_width = kernel_args['kernel_width']
        if kernel_type == "gaussian" or kernel_type == "g":
            sigma = kernel_args['sigma']
            kernel = np.arange(kernel_width ** 2).reshape((kernel_width, kernel_width))
            kernel = gaussian_filter(kernel, sigma=sigma)
            kernel = kernel / np.sum(kernel)
        elif kernel_type == "laplacian" or kernel_type == "l":
            kernel = self.create_laplacian_filter(kernel_width)
        elif kernel_type == "uniform" or kernel_type == "u":
            kernel = np.ones((kernel_width, kernel_width))
            kernel = kernel / np.sum(kernel)
        else:
            raise "Invalid kernel type requested"

        self.filter["description"] = kernel_type
        self.filter["kernel"] = kernel
        self.filter["kernel_width"] = kernel_width

    def applyFilter(self):
        pad_mode = "edge"  # "constant" for 0 padding, "edge" for nearest edge padding
        kernel = self.filter["kernel"]
        # bgr_padded = np.stack([np.pad(np.split(self.bgr_image, [1,2], 2)[x][:,:,0], r, pad_mode) for x in range(3)], axis=2)
        # l_padded = np.pad(np.split(self.hls_image, [1,2], 2)[1][:,:,0], r, pad_mode)
        #
        # s = self.bgr_image.shape
        # for x in range(s[0]):
        #     for y in range(s[1]):
        #         for c in range(s[2]):  # color channel
        #             self.bgr_image_filtered[x,y,c] = np.sum(k*bgr_padded[x:x+d,y:y+d,c])
        #         self.hls_image_filtered[x,y,1] = np.sum(k*l_padded[x:x+d,y:y+d])
        #
        # # normalize filtered images
        # for c in range(s[2]):
        #     self.bgr_image_filtered[:,:,c] = self.normalize(self.bgr_image_filtered[:,:,c], 256).clip(0,255)
        # self.hls_image_filtered[:,:,1] = self.normalize(self.hls_image_filtered[:,:,1], 256).clip(0,255)
        #


        # Pad top and bottom
        # rgb_padded = np.pad(self.bgr_image, 2, self.pad_with, padder=0)  # Replace 2 with proper filter value
        self.bgr_image_filtered = cv2.filter2D(self.bgr_image, -1, kernel)
        intensity_array = self.get_intensity_array(self.hls_image)
        intensity_array = cv2.filter2D(intensity_array, -1, kernel)
        for x in range(self.hls_image.shape[0]):
            for y in range(self.hls_image.shape[1]):
                self.hls_image_filtered[x][y][2] = intensity_array[x][y][0]

        self.filtered_difference = np.full(self.bgr_image.shape[:2], 127) \
            + cv2.cvtColor(self.bgr_image_filtered, cv2.COLOR_BGR2GRAY).astype(np.int32) \
            - self.hls_image_filtered[:,:,1]
        self.filtered_difference = self.filtered_difference.astype(np.uint8)

    def pad_with(self, vector, pad_width, iaxis, kwargs):
        pad_value = kwargs.get('padder', 10)
        vector[:pad_width[0]] = pad_value
        vector[-pad_width[1]:] = pad_value
        return vector

    def get_intensity_array(self, hsv_array):
        row = hsv_array.shape[0]
        col = hsv_array.shape[1]
        result = np.zeros((row, col, 3), dtype=np.uint8)
        for x in range(row):
            for y in range(col):
                result[x][y][0] = hsv_array[x][y][2] - 1
                result[x][y][1] = hsv_array[x][y][2] - 1
                result[x][y][2] = hsv_array[x][y][2] - 1
        return result

    def create_laplacian_filter(self, kernel_width=3):
        kernel = np.ones((kernel_width, kernel_width))
        total = np.sum(kernel) - 1
        height = kernel.shape[0]
        width = kernel.shape[1]
        kernel[int(height / 2)][int(width / 2)] = -1 * total
        kernel = kernel * -1
        return kernel

    def create_gaussian_filter(self, kernel_width=3, sigma=1):
        kernel = np.random.randint(50, size=(kernel_width, kernel_width))
        for x in range(kernel.shape[0]):
            for y in range(kernel.shape[1]):
                kernel[x][y] = self.gauss(kernel[x][y], sigma)
        return kernel

    def gauss(self, x, sigma=1):
        return int((1 / math.sqrt(2 * math.pi * (sigma ** 2))) * math.exp(-(x ** 2)/(2 * (sigma ** 2))))

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
        return cv2.cvtColor(self.hls_image_filtered, cv2.COLOR_HSV2BGR)

    def getProcessedDiff(self):
        return self.filtered_difference
