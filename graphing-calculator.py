# graphing calculator (made by Varicolour (varicolour on github))
import numpy as np
import matplotlib.pyplot as plt
import re
import warnings

red = "\033[31m"        # ANSI color codes, I just made them into variables so it's easy to work with
green = "\033[32m"
blue = "\033[34m"
yellow = "\033[33m"
magenta = "\033[35m"
cyan = "\033[36m"
bold = "\033[1m"
italic = "\033[3m"
underline = "\033[4m"
strikethrough = "\033[9m"
clear = "\033[0m"

def add_multiplication_operator(text):          # this looks for a pattern of a number and then a letter (2x, 3a, 7s etc.) and puts " * " in between. this is so you can write an equation like you would normally, but the computer can still understand it
    pattern = r'(\d+)([a-zA-Z]+)'
    result = re.sub(pattern, r'\1 * \2', text)
    return result

def replace_parts_of_equations(equationNumber): # replaces parts of an equation that it takes from the dictionary (where the equations are stored) with a number you give it. again, this is so the computer can understand it and you can write it normally
    equation = equations[f"y{equationNumber}"]
    if equation == "":
        return ""
    else:
        if "x" not in equation:
            equation += "+ 0x"   # workaround for when you want to plot an equation not containing "x" (adding + 0x makes sure the arrays are the same shape)
        if "sin" or "cos" or "tan" in equation:
            equation = " " + equation   # workaround so sin, cos and tan don't need to be case sensitive
        for old, new in replacements.items():
            equation = equation.replace(old, new)
        equation = add_multiplication_operator(equation)
        return equation

def plot_equations(equations, settings):
    calcXmax = int(settings["calc. x max."])     # these are made into variables to make it more readable
    calcXmin = int(settings["calc. x min."])
    precisionMultiplier = int(settings["precision multiplier"])

    x = np.linspace(calcXmin, calcXmax, ((calcXmax - calcXmin) * precisionMultiplier))    # generates an array of evenly spaced values between calcXmin and calcXmax, and assigns it to x
    try:
        plt.title(settings["plot title"])
        plt.xlabel(settings["x label"])
        plt.ylabel(settings["y label"])
        plt.axis((settings["window x min."], settings["window x max."], settings["window y min."], settings["window y max."]))
        for i, equation in enumerate(equations, start=1):
            if equations[f"y{i}"] != "":
                try:
                    y = eval(replace_parts_of_equations(i))  # Evaluate the equation
                    if y is not None:
                        plt.plot(x, y, color=settings[f"color y{i}"])  # Plot if evaluation succeeds
                except SyntaxError:
                    print(f"{red}{underline}[plot error]: syntax error in{clear} {green}{bold}y{i}{clear}")
                    pass  # Skip plotting if there's a syntax error in the equation
        plt.grid(True)
        plt.show()
    except Exception as e:
         print(f"\n{red}{underline}[plot error]: {e}{clear}")

def equations_menu():
    while True:
        print(f"\n{green}{bold}pick an equation below, press {magenta}[B]{clear}{green}{bold} to go back, or {magenta}[C]{clear}{green}{bold} to clear{clear}")

        for key, value in equations.items():
            print(f"{green}{bold}{key}{clear}: {value}") # prints all the equations and their keys (Y1, Y2 etc.)
        subMenuChoice = input("").lower()

        if subMenuChoice == "b":
            break
        if subMenuChoice == "c":
            for key, value in equations.items():
                equations[key] = ""
            continue

        try:
            print(f"\n{green}{bold}{subMenuChoice} is currently:{clear} {equations[subMenuChoice]}")
        except Exception as e:
            print(f"{red}{underline}[choice error]: {e}{clear}")
            continue

        equationChange = input(f"{green}{bold}change it to: {clear}").lower()
        equations[subMenuChoice] = equationChange

def settings_menu():
    while True:
        print(f"\n{blue}{bold}pick a setting below, or {magenta}[B]{clear}{blue}{bold} to go back{clear}")

        for key, value in settings.items():
            print(f"{blue}{bold}{key}{clear}: {value}")
        subMenuChoice = input("").lower()
        if subMenuChoice == "b":
            break

        try:
            print(f"\n{blue}{bold}{subMenuChoice} is currently:{clear} {settings[subMenuChoice]}")
        except Exception as e:
            print(f"{red}{underline}[choice error]: {e}{clear}")
            continue

        settingChange = input(f"{blue}{bold}change it to: {clear}")
        settings[subMenuChoice] = settingChange
        # this menu is the same as the equation one but for settings

def calculations_menu():
    while True:
        print(f"\n{red}{bold}pick a calculation below, or {magenta}[B]{clear}{red}{bold} to go back{clear}")

        for key, value in calculations.items():
            print(f"{red}{bold}{key}{clear}")
        subMenuChoice = input("").lower()
        if subMenuChoice == "b":
            break

        calculations[subMenuChoice]()
        # this menu is also the same

def calculate_value():
    print(f"\n{red}{bold}pick an equation below{clear}")    # pick an equation to find a value
    for key, value in equations.items():
        print(f"{green}{bold}{key}{clear}: {value}")          # print all the equations

    equationNumber = input("").lower()                              # type which one
    displayEquation = equations[equationNumber]                       # save the chosen equation for later
    equationNumber = int(equationNumber.replace("y", ""))   # remove the Y from the input

    x = float(input(f"\n{red}{bold}x = {clear}"))
    y = round(eval(replace_parts_of_equations(equationNumber)), 3)    # eval the chosen equation with replaced parts

    print(f"{red}{bold}the value for {green}{displayEquation}{red} at x = {clear}{x}{red}{bold} is{clear} {y}")       # print results

def calculate_zero():
    print(f"\n{red}{bold}pick an equation below{clear}")    # same as for the value calculation
    for key, value in equations.items():
        print(f"{green}{bold}{key}{clear}: {value}")

    equationNumber = input("").lower()
    displayEquation = equations[equationNumber]
    equationNumber = int(equationNumber.replace("y", ""))   # until here

    leftBound = int(input(f"\n{red}{bold}left bound{clear}: ")) # choose a left and right bound for where to calculate y = 0
    rightBound = int(input(f"{red}{bold}right bound{clear}: "))
    x = np.linspace(leftBound, rightBound, ((rightBound - leftBound) * settings["calculation precision multiplier"]))   # use the left and right bound to generate an x array
    y = eval(replace_parts_of_equations(equationNumber))    # eval with replaced parts

    yCloseToZero = np.where(np.abs(y) < 0.1)                # find where |y| < 0.1 (so where y is close to 0)

    if len(yCloseToZero[0] > 0):                            # if a point where |y| < 0.1 is found,
        correspondingX = x[yCloseToZero]                    # find the corresponding x values to these points
        meanCorrespondingX = np.mean(correspondingX)        # and calculate the mean of those
        print(f"\n{red}{bold}y = 0 between {clear}{leftBound} {red}{bold}and {clear}{rightBound}{red}{bold} in {green}{displayEquation}{red}{bold} at x = {clear}{round(meanCorrespondingX, 3)}")
    else:
        print(f"\n{red}{bold}no values have been found")

def calculate_intersect():
    print(f"\n{red}{bold}pick two equations below{clear}")    # same as for the zero calculation
    for key, value in equations.items():
        print(f"{green}{bold}{key}{clear}: {value}")

    equationNumber1 = input("equation 1: ").lower()
    equationNumber2 = input("equation 2: ").lower()
    displayEquation1 = equations[equationNumber1]
    displayEquation2 = equations[equationNumber2]
    equationNumber1 = int(equationNumber1.replace("y", ""))
    equationNumber2 = int(equationNumber2.replace("y", "")) # but this is all double because we need 2 equations

    leftBound = int(input(f"\n{red}{bold}left bound{clear}: ")) # choose a left and right bound for where to calculate y1 = y2
    rightBound = int(input(f"{red}{bold}right bound{clear}: "))
    x = np.linspace(leftBound, rightBound, ((rightBound - leftBound) * settings["calculation precision multiplier"]))   # use the left and right bound to generate an x array
    y1 = eval(replace_parts_of_equations(equationNumber1))
    y2 = eval(replace_parts_of_equations(equationNumber2))    # eval with replaced parts

    yIntersect = np.where(np.abs(y1 - y2) < 0.1)                # find where |y1 - y2| < 0.1 (so where y1 is close to y2)
    meanIntersectY = np.mean(y1[yIntersect])                    # take the mean of the y values of those indices

    if len(yIntersect[0]) > 0:                            # if a point where |y1 - y2| < 0.1 is found,
        correspondingX = x[yIntersect]                    # find the corresponding x values to these points
        meanCorrespondingX = np.mean(correspondingX)        # and calculate the mean of those
        print(f"\n{green}{bold}{displayEquation1}{red} and {green}{displayEquation2}{red} intersect at ({clear}{round(meanCorrespondingX, 3)}{red}{bold};{clear}{round(meanIntersectY, 3)}{red}{bold})")
    else:
        print(f"\n{red}{bold}no values have been found")

replacements = {
    " sin": "np.sin",
    " cos": "np.cos",
    " tan": "np.tan",
    "(sin": "(np.sin",
    "(cos": "(np.cos",
    "(tan": "(np.tan",
    "arcsin": "np.arcsin",
    "arccos": "np.arccos",      # things that are replaced in the equations so the computer understands them
    "arctan": "np.arctan",
    "^": " ** ",
    "sqrt": "np.sqrt",
    "pi": "np.pi",
    "e": "np.e",
    ")(": ") * ("
}

settings = {
    "window x min.": -10,        # these 4 settings are just for the display window's standard dimensions, you can pan and zoom when it's open, but these change what they are when it opens
    "window x max.": 10,
    "window y min.": -10,
    "window y max.": 10,
    "color y1": "red",   # colors for the 5 different input equations
    "color y2": "blue",
    "color y3": "green",
    "color y4": "orange",
    "color y5": "purple",
    "x label": "x",
    "y label": "y",
    "plot title": "plot",
    "calc. x min.": -1000,  # minimum X value from where the graph gets calculated
    "calc. x max.": 1000,   # maximum X value to where the graph gets calculated
    "precision multiplier": 100,  # how many float X values are generated in the array per integer (so a precisionMultiplier of 10 would be 10 floats per integer; 0,1 0,2 0,3 etc. and a precisionMultiplier of 100 would be 0,01 0,02 0,03 etc.)
    "calculation precision multiplier": 10000 # same as precision multiplier, but for calculations. this is normally set higher because it won't impact performance as much and precision is more important in this case
}

calculations = {
    "value": calculate_value,
    "zero": calculate_zero,
    "intersect": calculate_intersect
}

equations = {
    "y1": "",   # this is where you will fill in the equations, but on startup, they are empty
    "y2": "",
    "y3": "",
    "y4": "",
    "y5": ""
}

warnings.filterwarnings("ignore", message="invalid value encountered in ") # ignores warnings about invalid values (for example, a negative number in sqrt), so that they do not get displayed in the terminal when graphing an equation with some invalid x values

while True:
    print(f"\n{green}{bold}[I]{clear} input equations | {yellow}{bold}[P]{clear} plot | {red}{bold}[C]{clear} calculate | {blue}{bold}[S]{clear} settings | {magenta}{bold}[Q]{clear} quit")
    menuChoice = input("").lower()

    if menuChoice == "i":
        equations_menu()
        continue

    elif menuChoice == "p":
        plot_equations(equations, settings)
        continue

    elif menuChoice == "c":
        calculations_menu()
        continue

    elif menuChoice == "s":
        settings_menu()
        continue

    elif menuChoice == "q":
        break

    else:
        print(f"{red}{underline}[choice error]: please choose one of the options{clear}")
        continue