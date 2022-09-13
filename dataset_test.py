from __future__ import annotations
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def oldChatter():
    with open('/home/donbot/Documents/NLP/Project/NLP_ChatBot/train_light.json', 'r') as f:
        train_data = json.load(f)

    #print('question: ', train_data[0]['question'])
    #print(train_data[0]['annotations'][0]['qaPairs'][0]['answer'][0])
    print(train_data[2])
    b = True

    c = not b

    print(train_data[1]['annotations'][0]['type'])

    def printAnswer(key):
        if train_data[key]['annotations'][0]['type'] == 'singleAnswer':
            print('answer: ', train_data[key]['annotations'][0]['answer'][0])
        else:
            answers = train_data[key]['annotations'][0]['qaPairs']
            for i in answers:
                print('answer: ', i['answer'][0])

    for i in range(3):
        print('question: ', train_data[i]['question'])
        printAnswer(i)

class bot:
    def __init__(self):
            self.cb = ChatBot('foodBot')
            trainer = ChatterBotCorpusTrainer(self.cb)
            trainer.train('chatterbot.corpus.english.food', 'chatterbot.corpus.english.conversations')
    def respond(self, input):
        return self.cb.get_response(input)


def chatter():
    cb = ChatBot('foodBot')
    trainer = ChatterBotCorpusTrainer(cb)

    trainer.train('chatterbot.corpus.english.food', 'chatterbot.corpus.english.conversations', 'chatterbot.corpus.english.ai')
    print(cb.get_response('What is today'))

bot1 = bot()
bot2 = bot()

convo = []
convo.append(f'bot1: {bot1.respond("hamsters are weirdS")}')
for i in range(10):
    convo.append(f"bot2: {bot2.respond(convo[-1])}")
    convo.append(f"bot1: {bot1.respond(convo[-1])}")
for i in convo:
    print(i)
