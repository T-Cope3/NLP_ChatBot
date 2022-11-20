import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

import json
import pickle

import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Tons more comments can be here and more intuitive names
lemat = WordNetLemmatizer()
intentFile = open('intents.json').read()
jsonIntent = json.loads(intentFile)

# intents: different grouping types
# patterns: possible user interactions
words = []
documents = []
classes = []
for intentDict in jsonIntent['intents']:
    for pattern in intentDict['patterns']:

        # Tokenize every word
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        # Add words to the array documents w/ corresponding tag
        documents.append((tokens, intentDict['tag']))

        # adding classes to our class list
        if intentDict['tag'] not in classes:
            classes.append(intentDict['tag'])


itemsToIgnore = ['?', '!', '.', ',', '\'']
words = [lemat.lemmatize(word.lower()) for word in words if word not in itemsToIgnore]

pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))

# preparation for network training
print(f"Docs: {documents}")



# THESE VARS NEEEEED TO BE HERE SO THEY ARE RESET / PERSISTENT PROPERLY FOR EACH DOC
patternAndIntents = []
output_empty = list([0] * len(classes))
for doc in documents:
    # bag of words
    bag = []
    # list of tokens
    pattern_words = doc[0]
    # token lemmatization
    pattern_words = [lemat.lemmatize(word.lower()) for word in pattern_words]
    # if the word matches, I enter 1, otherwise 0
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_col = list(output_empty)
    output_col[classes.index(doc[1])] = 1
    patternAndIntents.append([bag, output_col])

training = np.array(patternAndIntents, dtype=object)
# creation of train and test sets: X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])

# model creation, can be smaller model tbh
# can make model more efficient too (what else?)
# do not need to load weights, model will predict based off saved model not weights
model = Sequential()
model.add(Dense(512, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Standard SGD, usually paired with Cat_Cross, but doesn't matter
# I have seen this overfit to failure, so using Adam for now
# sgd = SGD(learning_rate=0.01, weight_decay=1e-6, momentum=0.9, nesterov=True)

# Categorical_cross is specifically for labels and predictions so we are using it
# Optimizer matters a lot less
import datetime
log_dir = "./logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

model.compile(
    loss='categorical_crossentropy',
    optimizer= tf.keras.optimizers.Adam(learning_rate=0.001), #sgd
    
    metrics=['accuracy',tf.keras.metrics.Precision(),tf.keras.metrics.Recall()]
    )

# fitting and saving the model
# Launch in cmd with TensorFlow pip installed to get the dashboard
# tensorboard --logdir="C:\Users\Troy Cope\Desktop\PyProject\logs"

# Defining optimal callback items, early stopping will wait until absolutely necessary to cut off weights
earlyStop = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=10)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
# Model is training to match the patterns and intents, respectively
# Still tuning hyper params to feel good, will implement early stopping
history = model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, callbacks=[tensorboard_callback, earlyStop], verbose=1)
model.save('foodbotModel.h5', history)

print("All generation is completed!")

# score = model.evaluate(x_test, y_test, verbose = 0)
# print('Test loss:', score[0]) 
# print('Test accuracy:', score[1])