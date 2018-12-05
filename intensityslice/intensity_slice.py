import numpy as np


class IntSlice:

    # This function assumes the given image is either a 2 channel grayscale image
    # or a 3 channel image with identical values on each channel
    def get_sliced_img(self, input_image, slices, interval_colors):
        row = input_image.shape[0]
        col = input_image.shape[1]
        new_img = np.zeros((row, col, 3), np.uint8)

        if self.is_three_channel_image(input_image):
            # Color intervals except top most
            for slice_index in range(len(slices)):
                slice_intensity = slices[slice_index]
                prev_slice_intensity = slices[slice_index]
                if slice_index > 0:
                    prev_slice_intensity = slices[slice_index - 1]
                interval_color_split = interval_colors[slice_index].split(',')
                r = int(interval_color_split[0])
                g = int(interval_color_split[1])
                b = int(interval_color_split[2])
                for i in range(row):
                    for j in range(col):
                        input_image_intensity = self.get_input_image_intensity(input_image, i, j)
                        if slice_index == 0 and input_image_intensity <= slice_intensity:
                            new_img[i][j][0] = r
                            new_img[i][j][1] = g
                            new_img[i][j][2] = b
                        elif slice_index > 0 and slice_intensity >= input_image_intensity > prev_slice_intensity:
                            new_img[i][j][0] = r
                            new_img[i][j][1] = g
                            new_img[i][j][2] = b

            # Color top most interval
            last_slice_intensity = slices[-1]
            last_interval_color_split = interval_colors[-1].split(',')
            r = int(last_interval_color_split[0])
            g = int(last_interval_color_split[1])
            b = int(last_interval_color_split[2])
            for i in range(row):
                for j in range(col):
                    input_image_intensity = self.get_input_image_intensity(input_image, i, j)
                    if input_image_intensity > last_slice_intensity:
                        new_img[i][j][0] = r
                        new_img[i][j][1] = g
                        new_img[i][j][2] = b

        return new_img

    def is_three_channel_image(self, image):
        return len(image.shape) == 3

    def get_input_image_intensity(self, input_image, i, j):
        input_image_intensity = input_image[i][j]
        if self.is_three_channel_image(input_image):
            input_image_intensity = input_image[i][j][0]
        return input_image_intensity
