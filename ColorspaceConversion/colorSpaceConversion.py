import numpy as np
import math
import cv2

class colorSpaceConversion:
    def convertColorSpace(self, image, mode):
        # mode is 0 for RGB to HSV and 1 for HSV to RGB
        if (mode == 1):
            hsi_image = self.rgb_to_hsi_image(image)
            bgr_image = self.hsi_to_rgb_image(hsi_image)
            return [bgr_image[:, :, 2], bgr_image[:, :, 1], bgr_image[:, :, 0]]
        else:
            return self.RGB2HSI(image)

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

    def RGB2HSI_raw(self, image):
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
                if (red == green and green == blue):
                    H[x, y] = 0
                else:
                    top = .5 * ((red - green) + (red - blue))
                    bottom = ((red - green) ** 2) + ((red - blue) * (green - blue))
                    bottom = np.sqrt(bottom)
                    theta = np.arccos(top / bottom)
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
        return [H, S, I]

    def RGB2HSI(self, image):
        hsi_raw = self.RGB2HSI_raw(image)
        H = self.fullContrastStetch(np.round(hsi_raw[0]))
        S = self.fullContrastStetch(hsi_raw[1])
        I = self.fullContrastStetch(hsi_raw[2])
        return [H, S, I]

    def fullContrastStetch(self, image):
        P = (255 / (image.max() - image.min()))
        L = (-1 * image.min()) * P
        image = (P * image) + L
        return np.round(image)

    def rgb_to_hsi_image(self, bgr_image):
        hsi_channels = self.RGB2HSI_raw(bgr_image)
        hsi_image = cv2.merge((hsi_channels[0], hsi_channels[1], hsi_channels[2]))
        return hsi_image

    def hsi_to_rgb_image(self, hsi_image):
        result = np.zeros(hsi_image.shape)
        height, width = hsi_image.shape[:2]
        for x in range(height):
            for y in range(width):
                hue = hsi_image[x, y, 0]
                saturation = hsi_image[x, y, 1]
                intensity = hsi_image[x, y, 2]
                if hue < 120:
                    blue = intensity * (1 - saturation)
                    red = intensity * (1 + ((saturation * math.cos(math.radians(hue))) / math.cos(math.radians(60 - hue))))
                    green = 3 * intensity - (red + blue)
                elif hue < 240:
                    hue = hue - 120
                    red = intensity * (1 - saturation)
                    green = intensity * (1 + ((saturation * math.cos(math.radians(hue))) / math.cos(math.radians(60 - hue))))
                    blue = 3 * intensity - (red + green)
                else:
                    hue = hue - 240
                    green = intensity * (1 - saturation)
                    blue = intensity * (1 + ((saturation * math.cos(math.radians(hue))) / math.cos(math.radians(60 - hue))))
                    red = 3 * intensity - (green + blue)
                result[x, y, 0] = np.round(blue)
                result[x, y, 1] = np.round(green)
                result[x, y, 2] = np.round(red)
        result[result > 255] = 255
        return result
