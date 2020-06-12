# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 00:51:40 2020

@author: Admin
"""
import nltk
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.lancaster import LancasterStemmer
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

stemmer=LancasterStemmer()

model = pickle.load(open('cc_bot.pickle','rb'))
#tfv = pickle.load(open('tfv.pickle','rb'))
tfv=TfidfVectorizer(min_df=1,stop_words='english')

data=pd.read_csv("qna.csv")
questions=data['questions'].values
le = LE()

questions=data['questions'].values
X=[]



def cleanup(sentence):
    word_tok=nltk.word_tokenize(sentence)
    stemmed_words=[stemmer.stem(w) for w in word_tok]
    return "".join(stemmed_words)

for question in questions:
    X.append(cleanup(question))
    
Y=le.fit_transform(data['classes'])
X=tfv.fit_transform(X)

def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))
    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:
        ixs.append(i[1])

    return ixs[::-1]



def chat():
    cnt = 0
    print("PRESS Q to QUIT")
    print("TYPE \"DEBUG\" to Display Debugging statements.")
    print("TYPE \"STOP\" to Stop Debugging statements.")
    print("TYPE \"TOP5\" to Display 5 most relevent results")
    print("TYPE \"CONF\" to Display the most confident result")
    print()
    print()
    DEBUG = False
    TOP5 = False

    print("Bot: Hi, Welcome to our IP Program!")
    while True:
        usr = input("You: ")
    
        if usr.lower() == 'yes':
            print("Bot: Yes!")
            continue

        if usr.lower() == 'no':
            print("Bot: No?")
            continue

        if usr == 'DEBUG':
            DEBUG = True
            print("Debugging mode on")
            continue

        if usr == 'STOP':
            DEBUG = False
            print("Debugging mode off")
            continue

        if usr == 'Q':
            print("Bot: It was good to be of help.")
            break

        if usr == 'TOP5':
            TOP5 = True
            print("Will display 5 most relevent results now")
            continue

        if usr == 'CONF':
            TOP5 = False
            print("Only the most relevent result will be displayed")
            continue
#
        t_usr = tfv.transform([cleanup(usr.strip().lower())])
        class_ = le.inverse_transform(model.predict(t_usr))
#        print(class_)
        

        questionset = data[data['classes']==class_[0]]
#        print(questionset)
#        break
#        print(np.shape(t_usr))
        if DEBUG:
            print("Question classified under category:", class_)
            print("{} Questions belong to this class".format(len(questionset)))

        cos_sims = []
        for question in questionset['questions']:
            sims = cosine_similarity(tfv.transform([question]), t_usr)
            cos_sims.append(sims)
            
        ind = cos_sims.index(max(cos_sims))

        if DEBUG:
            question = questionset["questions"][questionset.index[ind]]
            print("Assuming you asked: {}".format(question))

        if not TOP5:
            print("Bot:", data['answers'][questionset.index[ind]])
        else:
            inds = get_max5(cos_sims)
            for ix in inds:
                print("Question: "+data['questions'][questionset.index[ix]])
                print("Answer: "+data['answers'][questionset.index[ix]])
                print('-'*50)

        print("\n"*2)
        outcome = input("Was this answer helpful? Yes/No: ").lower().strip()
        if outcome == 'yes':
            cnt = 0
        elif outcome == 'no':
            inds = get_max5(cos_sims)
            sugg_choice = input("Bot: Do you want me to suggest you questions ? Yes/No: ").lower()
            if sugg_choice == 'yes':
                q_cnt = 1
                for ix in inds:
                    print(q_cnt,"Question: "+data['questions'][questionset.index[ix]])
                    # print("Answer: "+data['Answer'][questionset.index[ix]])
                    print('-'*50)
                    q_cnt += 1
                num = int(input("Please enter the question number you find most relevant: "))
                print("\n Bot: ", data['answers'][questionset.index[inds[num-1]]])

chat()
