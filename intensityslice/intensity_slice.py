import cv2
import numpy as np


class IntSlice:
    input_image = None
    slice = None

    def __init__(self, image, slicing):
        """Read input image and convert to grayscale image"""
        self.input_image = cv2.imread(image, 0)
        """Set slice from input dict() of { slice (integer): RGB (list) }"""
        self.slice = slicing

    def get_sliced_img(self):
        """new_img will be the output image with colored slices"""
        row = self.input_image.shape[0]
        col = self.input_image.shape[1]
        new_img = np.zeros([row, col])

        for i in range(row):
            for j in range(col):
                new_img[i, j] = slice[-1]
        del(slice[-1])

        counter = 0
        for key in self.slice:
            for i in range(row):
                for j in range(col):
                    """If intensity at (i,j) is in interval, change it the color on new_img """
                    if key >= self.input_image[i, j] >= counter:
                        new_img[i, j] = key[0]
            counter = key + 1

        return new_img
