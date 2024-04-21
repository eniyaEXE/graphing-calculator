# graphing calculator (made by Eniya (EniyaEXE on github))
import itertools
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
    equation = equations[f"Y{equationNumber}"]
    for old, new in replacements.items():
        equation = equation.replace(old, new)
    equation = add_multiplication_operator(equation)
    return equation

def plot_equations():
    y1, y2, y3, y4, y5 = None, None, None, None, None   # sets all of them to None, so ones that can't get evaluated won't be plotted and won't raise an exception
    try:
        y1 = eval(replace_parts_of_equations(1))  # evaluates the equations (with the replaced parts) for every value in the array
    except SyntaxError:
        pass
    try:
        y2 = eval(replace_parts_of_equations(2))
    except SyntaxError:
        pass
    try:
        y3 = eval(replace_parts_of_equations(3))
    except SyntaxError:
        pass
    try:
        y4 = eval(replace_parts_of_equations(4))
    except SyntaxError:
        pass
    try:
        y5 = eval(replace_parts_of_equations(5))
    except SyntaxError:
        pass

    try:
        plt.title(settings["plot title"])
        plt.xlabel(settings["x Label"])
        plt.ylabel(settings["y Label"])
        plt.axis((settings["window X min."], settings["window X max."], settings["window Y min."], settings["window Y max."]))
        if y1 is not None:
            plt.plot(x, y1, color=settings["color Y1"])
        if y2 is not None:
            plt.plot(x, y2, color=settings["color Y2"])
        if y3 is not None:
            plt.plot(x, y3, color=settings["color Y3"])     # plots the graphs with the settings
        if y4 is not None:
            plt.plot(x, y4, color=settings["color Y4"])
        if y5 is not None:
            plt.plot(x, y5, color=settings["color Y5"])
        plt.grid(True)
        plt.show()
    except:
        print(f"\n{red}{bold}[plot error]{clear}")

def equations_menu():
    for _ in itertools.count():
        print(f"\n{green}{bold}pick an equation below, or {magenta}[B]{clear}{green}{bold} to go back{clear}")
        for key, value in equations.items():
            print(f"{green}{bold}{key}{clear}: {value}") # prints all the equations and their keys (Y1, Y2 etc.)
        subMenuChoice = input("")
        if subMenuChoice == "B":
            break
        try:
            print(f"\n{green}{bold}{subMenuChoice} is currently:{clear} {equations[subMenuChoice]}")
        except:
            print(f"{red}{bold}[choice error]{clear}")
            continue
        equationChange = input(f"{green}{bold}change it to: {clear}")
        equations[subMenuChoice] = equationChange

def settings_menu():
    for _ in itertools.count():
        print(f"\n{blue}{bold}pick a setting below, or {magenta}[B]{clear}{blue}{bold} to go back{clear}")
        for key, value in settings.items():
            print(f"{blue}{bold}{key}{clear}: {value}")
        subMenuChoice = input("")
        if subMenuChoice == "B":
            break
        try:
            print(f"\n{blue}{bold}{subMenuChoice} is currently:{clear} {settings[subMenuChoice]}")
        except:
            print(f"{red}{bold}[choice error]{clear}")
            continue
        settingChange = input(f"{blue}{bold}change it to: {clear}")
        settings[subMenuChoice] = settingChange
        # this menu is the same as the equation one but for settings

replacements = {
    "Sin": "np.sin",
    "Cos": "np.cos",
    "Tan": "np.tan",
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
    "window X min.": -10,        # these 4 settings are just for the display window's standard dimensions, you can pan and zoom when it's open, but these change what they are when it opens
    "window X max.": 10,
    "window Y min.": -10,
    "window Y max.": 10,
    "color Y1": "red",   # colors for the 5 different input equations
    "color Y2": "blue",
    "color Y3": "green",
    "color Y4": "orange",
    "color Y5": "purple",
    "x Label": "x",
    "y Label": "y",
    "plot title": "plot",
    "calc. X min.": -1000,  # minimum X value from where the graph gets calculated
    "calc. X max.": 1000,   # maximum X value to where the graph gets calculated
    "precision multiplier": 100  # how many float X values are generated in the array per integer (so a precisionMultiplier of 10 would be 10 floats per integer; 0,1 0,2 0,3 etc. and a precisonMultiplier of 100 would be 0,01 0,02 0,03 etc.)
}

equations = {
    "Y1": "",   # this is where you will fill in the equations, but on startup, they are of course empty
    "Y2": "",
    "Y3": "",
    "Y4": "",
    "Y5": ""
}

calcXmax = settings["calc. X max."]     # these are made into variables to make it more readable
calcXmin = settings["calc. X min."]
precisionMultiplier = settings["precision multiplier"]

warnings.filterwarnings("ignore", message="invalid value encountered in ") # ignores warnings about invalid values (for example, a negative number in sqrt), so that they do not get displayed in the terminal when graphing an equation with invalid x values
x = np.linspace(calcXmin, calcXmax, ((calcXmax - calcXmin) * precisionMultiplier))    # generates an array of evenly spaced values between calcXmin and calcXmax, and assigns it to x

for _ in itertools.count():
    print(f"\n{green}{bold}[A]{clear} input equations | {yellow}{bold}[B]{clear} plot | {red}{bold}[C]{clear} calculate | {blue}{bold}[D]{clear} settings")
    menuChoice = input("")

    if menuChoice == "A":
        equations_menu()
        continue

    elif menuChoice == "B":
        plot_equations()
        continue

    elif menuChoice == "C":
        input(f"{magenta}{bold}coming soon! :){clear}\n")
        continue

    elif menuChoice == "D":
        settings_menu()
        continue

    else:
        print(f"{red}{bold}[choice error]{clear}")
        continue