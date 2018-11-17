import math
import numpy as np

import simpleeval   # https://github.com/danthedeckie/simpleeval
# pip install simpleeval

class UserFuncEval:
    def __init__(self):
        other_functions = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "abs": abs}
        self.s = simpleeval.SimpleEval()
        self.all_functions = simpleeval.DEFAULT_FUNCTIONS.copy()
        self.all_functions.update(other_functions)
        self.s.names = {"x": np.arange(256)}
        self.output = None

    # input is a string of the user input function
    # returns false if unsuccessful parse. maybe set input font color to red while there is invalid input?
    def update(self, input, var_substitutions = None):
        if var_substitutions:  # and type(var_substitutions) == type(dict()):
            self.s.names = var_substitutions
            print("var_substitutions")
        
        # self.output = self.s.eval(input)
        try:
            self.output = self.s.eval(input)
        except:
            return False

        return True

    def getOutput(self):
        return self.output