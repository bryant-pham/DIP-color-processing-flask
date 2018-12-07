"""
warning: this class may raise exceptions
usage:
>>> from smoothensharpen import smoothenSharpen as sns
>>> sns = smoothensharpen.SmoothenSharpen(some_image)
>>> sns.loadKernel("gaussian")  # choose between "gaussian", "laplacian", "uniform"
>>> sns.filter["kernel"]  # check kernel if desired. note that it is rotated 180 degrees
>>> sns.applyFilter()
>>> filtered_bgr = sns.getProcessedBGR()
>>> filtered_hls = sns.getProcessedHSI()
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
from scipy.ndimage import gaussian_filter
from ColorspaceConversion import colorSpaceConversion

_ERR_GRAY_INPUT = "Grayscale image received; input image must be RGB or RGBA"

class SmoothenSharpen:
    def __init__(self, input_image):
        # images must be color
        self.bgr_image = np.zeros((1,1,3))
        self.converter = colorSpaceConversion.colorSpaceConversion()
        if len(input_image.shape) == 3:
            if input_image.shape[2] == 3:
                self.bgr_image = input_image
            elif input_image.shape[2] == 4:
                self.bgr_image = cv2.cvtColor(input_image, cv2.COLOR_BGRA2BGR)
            else:
                raise _ERR_GRAY_INPUT
        else:
            raise _ERR_GRAY_INPUT

        self.hsi_image = self.converter.rgb_to_hsi_image(self.bgr_image)

        self.bgr_image_filtered = self.bgr_image.copy()
        self.hsi_image_filtered = self.hsi_image.copy()
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
        self.filter["kernel"] = np.fliplr(np.flipud(kernel))
        self.filter["kernel_width"] = kernel_width

    def applyFilter(self):
        kernel = self.filter["kernel"]
        self.bgr_image_filtered = cv2.filter2D(self.bgr_image, -1, kernel)

        intensity_array = self.hsi_image_filtered[:, :, 2]
        intensity_array = intensity_array.astype(np.uint8)
        intensity_array_filtered = cv2.filter2D(intensity_array, -1, kernel)
        intensity_array_filtered = intensity_array_filtered.astype(np.uint8)
        self.hsi_image_filtered[:, :, 2] = intensity_array_filtered

        self.filtered_difference = np.full(self.bgr_image.shape[:2], 127) \
            + cv2.cvtColor(self.bgr_image_filtered, cv2.COLOR_BGR2GRAY).astype(np.int32) \
            - self.hsi_image_filtered[:, :, 2]
        self.filtered_difference = self.filtered_difference.astype(np.uint8)

    def create_laplacian_filter(self, kernel_width=3):
        kernel = np.ones((kernel_width, kernel_width))
        total = np.sum(kernel) - 1
        height = kernel.shape[0]
        width = kernel.shape[1]
        kernel[int(height / 2)][int(width / 2)] = -1 * total
        kernel = kernel * -1
        return kernel

    def getProcessedBGR(self):
        return self.bgr_image_filtered

    def getProcessedHSI(self):
        result = self.converter.hsi_to_rgb_image(self.hsi_image_filtered)
        return result

    def getProcessedDiff(self):
        return self.filtered_difference
