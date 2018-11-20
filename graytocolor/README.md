# GrayToColor
## Requires simpleeval:  
```bash
$ pip install simpleeval
```
---
## testg2c usage:
Assuming `Lenna.png` is in the root folder:  
```python
>>> from graytocolor.testg2c import *
>>> showImage(lenna)
>>> showImage(lenna_gray, "lenna - grayscale")
>>> testg2c()
>>> testg2c(preset=3)  # there are 10 presets! (located in GrayToColor.py)
>>> testg2c({"blue": "255-x", "green": "255-x", "red": "255-x"})
>>> testg2c("255-x", "255-x", "255-x")  # ordered as: blue, green, red
>>> showLastChannels()
>>> interactive(4)  # uses preset 4
```
---
## GrayToColor usage:  
```python
from graytocolor import GrayToColor as g2c
g2c = g2c.GrayToColor(lenna_img)
print("Valid operations: " + str(g2c.getValidOperations()))
# x is intensity of original image
# each function maps domain:[0-255] to range:[0-255]
if g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"}):
    processed_image = g2c.getProcessedImage()
else:
    # there is an invalid function. check g2c.valid_functions (dict) for the specific channel
    print("Valid functions: " + str(g2c.valid_functions))
processed_image_2 = g2c.getProcessedImage(g2c.presets[3])
g2c.loadImage(another_img)
```

---
## UserFuncEval usage:  
```python
from graytocolor import UserFuncEval as ufe
ufe = ufe.UserFuncEval()
ufe.s.names["my_var"] = list(range(12))
if ufe.update("cos(my_var / 6 * pi)"):
    ufe.getOutput()
else:
    # invalid function or parsing error
    pass
```
