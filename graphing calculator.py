# graphing calculator (made by Eniya (EniyaEXE on github))
import itertools
import numpy as np
import matplotlib.pyplot as plt
import re
import warnings

def add_multiplication_operator(text):
    pattern = r'(\d+)([a-zA-Z]+)'
    result = re.sub(pattern, r'\1 * \2', text)
    return result

replacementDict = {
    "Sin": "np.sin",
    "Cos": "np.cos",
    "Tan": "np.tan",
    "arcsin": "np.arcsin",
    "arccos": "np.arccos",
    "arctan": "np.arctan",
    "^": " ** ",
    "sqrt": "np.sqrt",
    "pi": "np.pi",
    "e": "np.e"
}

warnings.filterwarnings("ignore", message="invalid value encountered in ") # ignores warnings about invalid values (for example, a negative number in sqrt), so that they do not get displayed in the terminal when graphing an equation with sqrt, arcsin etc.

for _ in itertools.count():
    equation = input("\n[input your equation here]\n")     # inputs
    Xmin = int(input("\nX min: "))
    Xmax = int(input("X max: "))
    equationInput = equation      # this saves the original input for later to be displayed

    # Replaces parts of the equation, so that you don't have to type "np.sin" or "**" etc. but can instead use regular mathematical notation. The Sin etc. are capitalized to avoid interference with the arcsin etc. (and have to be inputted this way)
    for old, new in replacementDict.items():
        equation = equation.replace(old, new)

    equation = add_multiplication_operator(equation)

    x = np.linspace(-1000, 1000, 100000)    # generates an array of 100.000 evenly spaced values between -1000 and 1000, and assigns it to x
    y = eval(equation)                      # evaluates the equation (with the replaced parts) for every value in the array

    # Makes the matplotlib window for displaying the graph
    plt.title(f"Plot for {equationInput}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis((Xmin, Xmax, Xmin, Xmax))
    plt.plot(x, y)
    plt.grid(True)
    plt.show()