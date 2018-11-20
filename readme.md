Intensity Slicing

The IntSlice class will take an input image (both colored and grayscale images will work) and a dictionary and read them into the input_image and slice variables respectively.
The dictionary is formatted such that the keys are integers corresponding to the slice and the values are lists containing the RGB values.

For example, the dictionary would be like 
{ integer : (r, g, b) } 
{ 120 : (20, 40, 199), 175 : (0, 44, 123), ... }

The get_sliced_img function will return an image with the intensity slicing completed.

Example code:
from intensity_slice import IntSlice


slice_object = IntSlice(input.png, slices)
output_img = slice.object.get_sliced_img()

In this case, output_img is the resultant image to be shown.
