import nltk, json, random, pickle
from nltk.stem import WordNetLemmatizer
lemat = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('foodbotModel.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
engageDefault = True

# Need to comment and change this file a lot
# Hookup to frontend UI
# Make process for food req -> new trained model maybeeeeee?
# Tons more comments can be here and more intuitive names

# preprocess user input
# tokenizing and lamenting for less processing
def clean_up_sentence(sentence):
    wordsInSentence = nltk.word_tokenize(sentence)
    shortenedWords = [lemat.lemmatize(word.lower()) for word in wordsInSentence]
    return shortenedWords

# create bag of words
# just like text vector array shown in class
def bagOfWords(sentence, words, onPrint=True):
    shortenedWords = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for sents in shortenedWords:
        for index,word in enumerate(words):
            if word == sents:
                bag[index] = 1
                global engageDefault
                engageDefault = False
                if onPrint:
                    print(f"Word present in bag: {word}")
    return(np.array(bag))

def makePrediction(sentence, model):
    p = bagOfWords(sentence, words, onPrint=False)
    res = model.predict(np.array([p]), verbose=0)[0]

    # print(f"res: {res} from {classes}")
    # Can adjust error as necessary, most common might be .6 vs .4 or less competitive.
    # .25 is fine for now but can be heightend for more certainty
    REMOVE_THRESHOLD = 0.25
    return_list = []
    global engageDefault

    if not engageDefault:
        results = [[i,r] for i,r in enumerate(res) if r>REMOVE_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        for r in results:
            # Spitting back the most likely w/ probability
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    else:
        return_list.append({"intent": "default", "probability": str(1)})
    engageDefault = True
    return return_list

def getResponse(pred, jsonIntent):
    # currently defaulting to whatever model predicts most highly
    # 
    tag = pred[0]['intent']
    intentList = jsonIntent['intents']
    for intent in intentList:
        if(intent['tag'] == tag):
            result = random.choice(intent['responses'])
            break
    return result

def messageFromAI(userMessage):
    pred = makePrediction(userMessage, model)
    # print(f"Calculated Data from calc_pred: {ints}")
    res = getResponse(pred, intents)
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

def ChatBotWithHistory():
    mainOutputWidth = 160
    #New windows with style
    sg.ChangeLookAndFeel('GreenTan')

    #Need to use monospace font in order to ensure the windowSize claculation remains true
    layout =  [[sg.Text('Your output will go here', size=(40, 1))],
                [sg.Multiline(size=(mainOutputWidth, 30), disabled = True, reroute_stdout=True, font=('Consolas 10'),
                 key='mainChat', do_not_clear=True)],
                [sg.T('Command History'), sg.T('', size=(20,3), key='history')],
                [sg.Multiline(size=(100, 6), enter_submits=True, key='query', do_not_clear=False),
                sg.Button('SEND', size=(10,5), border_width=5, button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
                sg.Button('EXIT', size=(10,5), border_width=5, button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('FoodBot Chatterface', default_element_size=(30, 2), font=('Helvetica',' 12'), default_button_element_size=(8,2), return_keyboard_events=True).Layout(layout)
    #Snagging user input and spitting back
    command_history = []
    history_offset = 0
    while True:
        (event, value) = window.Read()
        if event == 'SEND':
            query = value['query'].rstrip()
            # EXECUTE YOUR COMMAND HERE
            print(("USER: {}".format(query)).rjust(mainOutputWidth))
            command_history.append(query)
            history_offset = len(command_history)-1
            window.find_element('query').Update('')
            # manually clear input because keyboard events blocks clear
            window.find_element('history').Update('\n'.join(command_history[-3:]))

            userInput = query
            response = messageFromAI(userInput)
            print("BOT: {}".format(response))
            window.find_element('query').Update('')
                
        #Quits if X clicked or Exit is pressed
        elif event in (None, 'EXIT'):
            break
        elif 'Up' in event and len(command_history):
            command = command_history[history_offset]
            # decrement is not zero
            history_offset -= 1 * (history_offset > 0)
            window.find_element('query').Update(command)
        elif 'Down' in event and len(command_history):
            # increment up to end of list
            history_offset += 1 * (history_offset < len(command_history)-1) 
            command = command_history[history_offset]
            window.find_element('query').Update(command)
        elif 'Escape' in event:
            window.find_element('query').Update('')
    window.close()

# Calls UI with the model implemented
ChatBotWithHistory() 
