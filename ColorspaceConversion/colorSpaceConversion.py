import numpy as np
import math
import cv2

class colorSpaceConversion:
    def convertColorSpace(self, image, mode):
        # mode is 0 for RGB to HSV and 1 for HSV to RGB
        if (mode == 1):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            return self.HSV2RGB(image)
        else:
            return self.RGB2HSV(image)

    def HSV2RGB(self, image):
        # get the size of my image
        height, width = image.shape[:2]

        # create my three channels
        R = np.zeros((height, width))
        G = np.zeros((height, width))
        B = np.zeros((height, width))

        # normalize values
        H = np.zeros((height, width), dtype= np.float_)
        for x in range(height):
            for y in range(width):
                H[x, y] = image[x, y, 0] * 2

        S = image[:, :, 1] / 255
        V = image[:, :, 2] / 255

        for x in range(height):
            for y in range(width):
                C = V[x, y] * S[x, y]
                X = C * (1 - np.abs((H[x, y] / 60) % 2 - 1))
                m = V[x, y] - C

                if (H[x, y] < 60):
                    var_r = C
                    var_g = X
                    var_b = 0
                elif (H[x, y] < 120):
                    var_r = X
                    var_g = C
                    var_b = 0
                elif (H[x, y] < 180):
                    var_r = 0
                    var_g = C
                    var_b = X
                elif (H[x, y] < 240):
                    var_r = 0
                    var_g = X
                    var_b = C
                elif (H[x, y] < 300):
                    var_r = X
                    var_g = 0
                    var_b = C
                else:
                    var_r = C
                    var_g = 0
                    var_b = X

                R[x, y] = (var_r + m) * 255
                G[x, y] = (var_g + m) * 255
                B[x, y] = (var_b + m) * 255

        return [R, G, B]

    def RGB2HSV(self, image):
        # get the size of my image
        height, width = image.shape[:2]

        # create my three channels
        H = np.zeros((height, width))
        S = np.zeros((height, width))
        V = np.zeros((height, width))

        for x in range(0, height):
            for y in range(0, width):
                blue = (image[x, y, 0]) / 255
                green = (image[x, y, 1]) / 255
                red = (image[x, y, 2]) / 255

                # top and bottom for arccos
                Cmax = np.amax([blue, green, red])
                Cmin = np.amin([blue, green, red])

                delta = Cmax - Cmin
                if (delta == 0):
                    H[x, y] = 0
                elif (Cmax == red):
                    H[x, y] = 60 * (((green - blue) / delta) % 6)
                elif (Cmax == green):
                    H[x, y] = 60 * (((blue - red) / delta) + 2)
                else:
                    H[x, y] = 60 * (((red - green) / delta) + 4)

                if (Cmax == 0):
                    S[x, y] = 0
                else:
                    S[x, y] = delta / Cmax

                V[x, y] = Cmax

        H = self.fullContrastStetch(H)
        S = self.fullContrastStetch(S)
        V = self.fullContrastStetch(V)

        return [H, S, V]

    def RGB2HSI(self, image):
        # get the size of my image
        height, width = image.shape[:2]

        # create my three channels
        H = np.zeros((height, width))
        S = np.zeros((height, width))
        I = np.zeros((height, width))

        for x in range(0, height):
            for y in range(0, width):
                # work on the H channel


                # get each channel value at the designated pixel
                blue = int(image[x, y, 0])
                green = int(image[x, y, 1])
                red = int(image[x, y, 2])

                # top and bottom for arccos
                if(red == green and green == blue):
                    H[x, y] = 0
                else:
                    top = .5 * ((red - green) + (red - blue))
                    bottom = ((red - green) ** 2) + ((red - blue) * (green - blue))
                    bottom = np.sqrt(bottom)
                    theta = np.arccos(top/bottom)
                    if (not (math.isfinite(theta))):
                        theta = 0
                    theta = theta * (180 / np.pi)
                    # assignment
                    if (blue <= green):
                        H[x, y] = theta
                    else:
                        H[x, y] = 360 - theta

                # work on the S channel

                # value checking
                if ((red + green + blue) == 0):
                    S[x, y] = 0
                else:
                    S[x, y] = (1 - ((3 / (red + green + blue)) * np.amin([red, blue, green])))

                # work on the I channel
                I[x, y] = ((1 / 3) * (red + blue + green))

        # preform a full contrast stretch on all generated channels
        H = self.fullContrastStetch(np.round(H))
        S = self.fullContrastStetch(S)
        I = self.fullContrastStetch(I)

        return [H, S, I]

    def fullContrastStetch(self, image):
        # get the size of my image
        height, width = image.shape[:2]

        # find the minimum and maximum
        maximum = np.NINF
        minimum = np.Inf
        for x in range(0, height):
            for y in range(0, width):
                value = image[x, y]
                if (value < minimum):
                    minimum = value
                if (value > maximum):
                    maximum = value

        # calculate P and L values
        P = (255 / (maximum - minimum))
        L = (-minimum) * P

        image = (P * image) + L
        return np.round(image)