# GrayToColor
## Requires simpleeval:  
```python
pip install simpleeval
```
---
## tester<span>.py</span> usage:
```
$ python tester.py
or
>>> from tester import *
>>> main()
```
---
## GrayToColor usage:  
```python
import GrayToColor as g2c
g2c = g2c.GrayToColor(lenna_img)
if g2c.updateImage({"blue": "255 - x", "green": "x", "red": "255 - x"}):  # x is intensity of original image
    processed_image = g2c.getProcessedImage()
else:
    # there is an invalid function. check g2c.valid_functions (dict) for the specific channel
    pass
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