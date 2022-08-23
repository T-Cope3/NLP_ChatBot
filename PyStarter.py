#This program is dedicated to a chatbot.

#Need to insall pip if not already: https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-for-installing-packages
#Need to install PySimpleGUI: pip install PySimpleGUI
#https://vimsky.com/zh-tw/examples/detail/python-method-PySimpleGUI.Multiline.html

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


#Chinese GAP
# # 需要導入模塊: import PySimpleGUI [as 別名]
# # 或者: from PySimpleGUI import Multiline [as 別名]
# def ChatBotWithHistory():
#     # -------  Make a new Window  ------- #
#     sg.ChangeLookAndFeel('GreenTan')            # give our form a spiffy set of colors

#     layout =  [[sg.Text('Your output will go here', size=(40, 1))],
#                 [sg.Output(size=(127, 30), font=('Helvetica 10'))],
#                 [sg.T('Command History'), sg.T('', size=(20,3), key='history')],
#                 [sg.Multiline(size=(85, 5), enter_submits=True, key='query', do_not_clear=False),
#                 sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
#                 sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

#     window = sg.Window('Chat window with history', default_element_size=(30, 2), font=('Helvetica',' 13'), default_button_element_size=(8,2), return_keyboard_events=True).Layout(layout)

#     # ---===--- Loop taking in user input and using it  --- #
#     command_history = []
#     history_offset = 0
#     while True:
#         (event, value) = window.Read()
#         if event == 'SEND':
#             query = value['query'].rstrip()
#             # EXECUTE YOUR COMMAND HERE
#             print('The command you entered was {}'.format(query))
#             command_history.append(query)
#             history_offset = len(command_history)-1
#             window.FindElement('query').Update('')                       # manually clear input because keyboard events blocks clear
#             window.FindElement('history').Update('\n'.join(command_history[-3:]))
#         elif event in (None, 'EXIT'):            # quit if exit event or X
#             break
#         elif 'Up' in event and len(command_history):
#             command = command_history[history_offset]
#             history_offset -= 1 * (history_offset > 0)      # decrement is not zero
#             window.FindElement('query').Update(command)
#         elif 'Down' in event and len(command_history):
#             history_offset += 1 * (history_offset < len(command_history)-1) # increment up to end of list
#             command = command_history[history_offset]
#             window.FindElement('query').Update(command)
#         elif 'Escape' in event:
#             window.FindElement('query').Update('')

#     sys.exit(69) 