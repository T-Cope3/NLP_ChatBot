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
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# create bag of words
def bagOfWords(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def calc_pred(sentence, model):
    p = bagOfWords(sentence, words,show_details=True)
    res = model.predict(np.array([p]))[0]

    # print(f"res: {res}")
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # print(f"Current results: {results}")
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    # currently defaulting to the first option
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

user = ''
print('Welcome! To quit, type "quit"')

while True:
    user = str(input(""))
    # kicks out of program if user enters quit
    exit() if user=='quit' else False
    # spits back the most prob response from AI
    res = send(user)
    print('AI:' + res)