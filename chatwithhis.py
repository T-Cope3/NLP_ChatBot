import PySimpleGUI as sg
# 需要導入模塊: import PySimpleGUI [as 別名]
# 或者: from PySimpleGUI import Multiline [as 別名]
def ChatBotWithHistory():
    mainOutputWidth = 160;
    # -------  Make a new Window  ------- #
    sg.ChangeLookAndFeel('GreenTan')            # give our form a spiffy set of colors

    #Need to use monospace font in order to ensure the windowSize claculation remains true
    layout =  [[sg.Text('Your output will go here', size=(40, 1))],
                [sg.Multiline(size=(mainOutputWidth, 30), disabled = True, reroute_stdout=True, font=('Consolas 10'),
                 key='mainChat', do_not_clear=True)],
                [sg.T('Command History'), sg.T('', size=(20,3), key='history')],
                [sg.Multiline(size=(100, 6), enter_submits=True, key='query', do_not_clear=False),
                sg.Button('SEND', size=(10,5), border_width=5, button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
                sg.Button('EXIT', size=(10,5), border_width=5, button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('ChatBot Simplification', default_element_size=(30, 2), font=('Helvetica',' 12'), default_button_element_size=(8,2), return_keyboard_events=True).Layout(layout)


    #rjust, pyton padding, for total characters

    #---===---Loop taking in user input and using it---#
    userFlag = True
    command_history = []
    history_offset = 0
    while True:
        (event, value) = window.Read()
        if event == 'SEND':
            query = value['query'].rstrip()
            # EXECUTE YOUR COMMAND HERE
            if(userFlag):
                print(("USER: {}".format(query)).rjust(mainOutputWidth))
                command_history.append(query)
                history_offset = len(command_history)-1
                window.find_element('query').Update('')                 # manually clear input because keyboard events blocks clear
                window.find_element('history').Update('\n'.join(command_history[-3:]))
                
            else:
                print("BOT: {}".format(query))
                window.find_element('query').Update('') 

            userFlag = not userFlag
        elif event in (None, 'EXIT'):            # quit if exit event or X
            break
        elif 'Up' in event and len(command_history):
            command = command_history[history_offset]
            history_offset -= 1 * (history_offset > 0)      # decrement is not zero
            window.find_element('query').Update(command)
        elif 'Down' in event and len(command_history):
            history_offset += 1 * (history_offset < len(command_history)-1) # increment up to end of list
            command = command_history[history_offset]
            window.find_element('query').Update(command)
        elif 'Escape' in event:
            window.find_element('query').Update('')
    window.close()

#sys.exit(69) 
ChatBotWithHistory()