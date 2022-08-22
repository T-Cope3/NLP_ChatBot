#This program is dedicated to a chatbot.

#Need to insall pip if not already: https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-for-installing-packages
#Need to install PySimpleGUI: pip install PySimpleGUI

#Good source https://realpython.com/pysimplegui-python/

import PySimpleGUI as sg

#sg.Window(title="Hi My Friends!", layout=[[]], margins=(100,50)).read();

# txt2=""
# #Initialize a holder variable 
# fruits=['apple', 'orange', 'pears', 'tomatoes']

# #Convert from List to Text with New line
# for i in fruits:txt2=f"{fruits}{i}\n"

# #Create layout
# layout2 = [[sg.Multiline(txt2,size=(28,28),key='-Items-'),],[sg.Ok()] ]

# #Single shot Popup Window
# sg.Window('Scroll to see the whole list of fruits', layout2,finalize=True).read(close=True)

import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("What's your name?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()