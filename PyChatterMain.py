import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('foodbotModel.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

#Need to comment and change this file a lot
#Hookup to frontend UI
#Make process for food req -> new trained model maybeeeeee?
# Tons more comments can be here and more intuitive names

# preprocess user input
# tokenizing and lamenting for less processing
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# create bag of words
# just like text vector array shown in class
def bagOfWords(sentence, words, onPrint=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if onPrint:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def calc_pred(sentence, model):
    p = bagOfWords(sentence, words, onPrint=False)
    res = model.predict(np.array([p]), verbose=0)[0]

    print(f"res: {res} from {classes}")
    # Can adjust error as necessary, most common might be .6 vs .4 or less competitive.
    # .25 is fine for now but can be heightend for more certainty
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        # Spitting back the most likely w/ probability
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    # currently defaulting to whatever model predicts most highly
    # 
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def send(msg):
    ints = calc_pred(msg, model)
    print(f"Calculated Data from calc_pred: {ints}")
    res = getResponse(ints, intents)
    return res

# user = ''
# print('Welcome! To quit, type "quit"')

# while True:
#     user = str(input(""))
#     # kicks out of program if user enters quit
#     exit() if user=='quit' else False
#     # spits back the most prob response from AI
#     res = send(user)
#     print('AI:' + res)


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

                userInput = query
                res = send(userInput)
                print("BOT: {}".format(res))
                window.find_element('query').Update('')
                
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



#rjust, pyton padding, for total characters
ChatBotWithHistory() 
