import numpy as np
import math
import cv2

class colorSpaceConversion:
    def convertColorSpace(self, image, mode):
        # mode is 0 for RGB to HSI and 1 for HSI to RGB
        if (mode == 1):
            C1, C2, C3 = self.RGB2HSI(image)
            image = cv2.merge((C1, C2, C3))
            return self.HSI2RGB(image)
        else:
            return self.RGB2HSI(image)

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
                blue = float(image[x, y, 0]/255)
                green = float(image[x, y, 1]/255)
                red = float(image[x, y, 2]/255)
                Cmin = np.amin([red, blue, green])
                Cmax = np.amax([red, blue, green])

                # top and bottom for arccos
                if(red == green and green == blue):
                    H[x, y] = 0
                else:
                    if(red == Cmax):
                        H[x, y] = 60 * (((green - blue) / (Cmax - Cmin)) % 6)
                    elif(green == Cmax):
                        H[x, y] = 60 * (((blue - red) / (Cmax - Cmin)) + 2)
                    else:
                        H[x, y] = 60 * (((red - green) / (Cmax - Cmin)) + 4)

                # work on the S channel

                # value checking
                if ((red + green + blue) == 0):
                    S[x, y] = 0
                else:
                    S[x, y] = (1 - ((3 / (red + green + blue)) * np.amin([red, blue, green])))

                # work on the I channel
                I[x, y] = ((1 / 3) * (red + blue + green))

        # preform a full contrast stretch on all generated channels
        S = self.fullContrastStetch(S)
        I = self.fullContrastStetch(I)

        return [H, S, I]

    def HSI2RGB(self, image):
        # get the size of my image
        height, width = image.shape[:2]

        # create my three channels
        R = np.zeros((height, width))
        G = np.zeros((height, width))
        B = np.zeros((height, width))

        for x in range(0, height):
            for y in range(0, width):
                # work on the H channel


                # get each channel value at the designated pixel
                Hue = float(image[x, y, 0])
                Sat = float(image[x, y, 1])/255
                Inten = float(image[x, y, 2])/255

                if(Hue>=240):
                    Hue = Hue - 240
                    Hue = np.deg2rad(Hue)
                    G[x, y] = Inten * (1 - Sat)
                    B[x, y] = Inten * (1 + ((Sat * np.cos(Hue)) / (np.cos(1.0472 - Hue))))
                    R[x, y] = (3 * Inten) - (G[x, y] + B[x, y])
                elif (Hue >= 120):
                    Hue = Hue - 120
                    Hue = np.deg2rad(Hue)
                    R[x, y] = Inten * (1 - Sat)
                    G[x, y] = Inten * (1 + ((Sat * np.cos(Hue)) / (np.cos(1.0472 - Hue))))
                    B[x, y] = (3 * Inten) - (R[x, y] + G[x, y])
                else:
                    Hue = np.deg2rad(Hue)
                    B[x, y] = Inten * (1 - Sat)
                    R[x, y] = Inten * (1 + ((Sat * np.cos(Hue)) / (np.cos(1.0472 - Hue))))
                    G[x, y] = (3 * Inten) - (R[x, y] + B[x, y])




        # preform a full contrast stretch on all generated channels
        R = self.fullContrastStetch(R)
        G = self.fullContrastStetch(G)
        B = self.fullContrastStetch(B)

        return [R, G, B]

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