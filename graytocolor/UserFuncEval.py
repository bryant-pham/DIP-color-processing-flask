import numpy as np
import ast

import simpleeval   # https://github.com/danthedeckie/simpleeval
"""
$ pip install simpleeval
"""

class UserFuncEval:
    def __init__(self):
        other_functions = {"sin": np.sin, "cos": np.cos, "tan": np.tan, "abs": abs}
        other_functions.update({"mod": np.mod, "sign": np.sign, "floor": np.floor, "ceil": np.ceil})
        self.s = simpleeval.SimpleEval()
        self.s.operators[ast.Mult] = np.multiply
        self.s.operators[ast.Pow] = np.power
        self.s.operators[ast.Mod] = np.mod
        self.s.functions = simpleeval.DEFAULT_FUNCTIONS.copy()
        del self.s.functions["str"]
        del self.s.functions["rand"]
        del self.s.functions["randint"]
        self.s.functions.update(other_functions)
        self.s.names = {"x": np.arange(256), "pi": np.pi}
        self.output = None

    # input is a string of the user input function
    # returns false if unsuccessful parse. maybe set input font color to red while there is invalid input?
    def update(self, input, var_substitutions = None):
        if var_substitutions:
            self.s.names.update(var_substitutions)
        
        try:
            self.output = self.s.eval(input)
        except:
            return False

        return True

    def getOutput(self):
        return self.output

    def getValidOperations(self):
        return set(self.s.functions.keys())
