# graphing calculator (made by Eniya (EniyaEXE on github))
import itertools
import numpy as np
import matplotlib.pyplot as plt

for _ in itertools.count():
    equation = input("\n[input your equation here]\n")     # inputs
    Xmin = int(input("\nX min: "))
    Xmax = int(input("X max: "))
    equationInput = equation      # this saves the original input for later to be displayed

    # Replaces parts of the equation, so that you don't have to type "np.sin" or "**" etc. but can instead use regular mathematical notation. The Sin etc. are capitalized to avoid interference with the arcsin etc. (and have to be inputted this way)
    equation = equation.replace("Sin", "np.sin")
    equation = equation.replace("Cos", "np.cos")
    equation = equation.replace("Tan", "np.tan")
    equation = equation.replace("arcsin", "np.arcsin")
    equation = equation.replace("arccos", "np.arccos")
    equation = equation.replace("arctan", "np.arctan")
    equation = equation.replace("^", " ** ")
    equation = equation.replace("sqrt", "np.sqrt")

    x = np.linspace(-1000, 1000, 100000)    # generates an array of 100.000 evenly spaced values between -1000 and 1000, and assigns it to x
    y = eval(equation)                       # evaluates the equation (with the replaced parts) for every value in the array

    # Makes the matplotlib window for displaying the graph
    plt.title(f"Plot for {equationInput}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis((Xmin, Xmax, Xmin, Xmax))
    plt.plot(x, y)
    plt.grid(True)
    plt.show()