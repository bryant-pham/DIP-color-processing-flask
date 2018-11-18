# GrayToColor
## Requires simpleeval:  
```bash
$ pip install simpleeval
```
---
## testg2c usage:
Place `lenna.png` into this folder.  
```python
>>> from testg2c import *
>>> showImage(lenna)
>>> showImage(lenna_gray, "lenna - grayscale")
>>> testg2c()
>>> testg2c(preset=3)
>>> testg2c({"blue": "255-x", "green": "255-x", "red": "255-x"})
>>> testg2c("255-x", "255-x", "255-x")  # order: blue, green, red
```
---
## GrayToColor usage:  
```python
import GrayToColor as g2c
g2c = g2c.GrayToColor(lenna_img)
# x is intensity of original image:
if g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"}):
    processed_image = g2c.getProcessedImage()
else:
    # there is an invalid function. check g2c.valid_functions (dict) for the specific channel
    print("Valid functions: " + g2c.valid_functions)
processed_image_2 = g2c.getProcessedImage(g2c.presets[3])
```

---
## UserFuncEval usage:  
```python
import UserFuncEval as ufe
ufe = ufe.UserFuncEval()
ufe.s.names["my_var"] = list(range(12))
if ufe.update("cos(my_var / 6 * pi)"):
    ufe.getOutput()
else:
    # invalid function or parsing error
    pass
```
