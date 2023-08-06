#Imports

import webbrowser
from pynotifier import Notification
import time
import pyautogui
import psutil as psu
import pywhatkit
import wikipedia

# User Guide

def UserGuide():
    print('''
    
    ## How to use 'useitpremade':
    Step1 -> pip install usitpremade
    step2 -> from useitpremade import *
    Then, Enjoy your autocode

    ## Functins to use:

    UserGuide() :: A Complete Guide For Freshers
    WebOpen() :: Open Inputed URL
    WebSearch() :: Search Inputed Query
    SenNot() :: Send Notification for Inputed Title and Description for 5 Seconds
    CreateProject() :: Create a Text File Project of Inputed Project Name and Descriptions
    OpenApps() :: Open Any Inputed App
    CheckBattery() :: Check Battery status for Laptops
    twoCalc() :: Two Digit Operator Calculator
    threeCalc() :: Three Digit Operator Calculator

    ## Release of useitpremade_two

    useitpremade_two is an Advanced Version of useitpremade
    and will be released in the month of March if useitpremade
    gets a good responce

    ''')

#Web Related

def WebOpen():
    url = input("Enter URL: ")
    webbrowser.open(url)

def WebSerach():
    search = input("What to Search: ")
    print("This is what i found on web...")

    try:
        pywhatkit.search(search)
        result = wikipedia.summary(search, 3)
        print(result)
        
    except:
        print(f"Sorry Sir. Data not available for {search}")

#Sending Notification

def SendNot():
    title = input("Notification Title: ")
    notification = input("Notification Description: ")
    Notification(title, notification, duration=5).send()
    time.sleep(2)
    print("Notification Successfully Sended")

# New Projects

def CreateProject():
    pr_name = input("New Projects Name: ")
    pr_des = input("Description of the Project: ")
    print(f"\nProject saved in the projects directory as {pr_name}")

    with open(f"{pr_name}.txt", "w") as f:
            f.write(f"Project: {pr_name}\n\n")
            f.write(f"Descriptions: {pr_des}")

# OPEN APPS

def OpenApps():
    appName = input("Name of the App: ")
    pyautogui.press('super')
    pyautogui.typewrite(appName)
    pyautogui.sleep(1)
    pyautogui.press('enter')

# Check Battery Level

def CheckBattery():
    battery = psu.sensors_battery()
    percent = battery.percent
    print(f"Battery Level is: {percent}%")

# Calculator: 2 Digit

def twoCalc():
    num1 = float(input("Number 1: "))
    num2 = float(input("Number 2: "))

    operator = input("Operator: ")

    if operator == '+':
        ans = num1+num2
        print(ans)

    elif operator == "-":
        ans = num1-num2
        print(ans)

    elif operator == "*":
        ans = num1*num2
        print(ans)

    elif operator == "/":
        ans = num1/num2
        print(ans)

    else: print(f"No such Operator Found for {operator}")

# Calculator: 3 Digit

def threeCalc():
    num1 = float(input("Number 1: "))
    operator1 = input("Operator For Num1 and Num2: ")
    num2 = float(input("Number 2: "))

    if operator1 == '+':
        num2 = num1+num2

    elif operator1 == "-":
        num2 = num1-num2

    elif operator1 == "*":
        num2 = num1*num2

    elif operator1 == "/":
        num2 = num1/num2

    else: print(f"No such Operator Found for {operator1}")

    operator2 = input("Operator for Number 2 and Number 3: ")
    num3 = float(input("Number 3: "))

    if operator2 == '+':
        ans = num2+num3
        print(ans)

    elif operator2 == "-":
        ans = num2-num3
        print(ans)

    elif operator2 == "*":
        ans = num2*num3
        print(ans)

    elif operator2 == "/":
        ans = num2/num3
        print(ans)

    else: print(f"No such Operator Found for {operator2}")