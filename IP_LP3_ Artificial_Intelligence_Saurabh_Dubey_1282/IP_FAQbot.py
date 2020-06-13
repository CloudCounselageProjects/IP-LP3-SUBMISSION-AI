import pandas as pd
import numpy as np
import pickle
import operator
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
from nltk.stem.lancaster import LancasterStemmer


stemmer = LancasterStemmer()
def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]

    return ' '.join(stemmed_words)


le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv('IP_Interns_FAQs.csv',encoding='latin1')
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)
y = le.transform(data['Class'])


trainx, testx, trainy, testy = tts(X, y, test_size=.20, random_state=0)

model = SVC(kernel='linear')
model.fit(trainx, trainy)
print("SVC:", model.score(testx, testy))


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
    print()
    print()
    DEBUG = False
    TOP5 = False

    print("Cloud Counselage Brtrix Chat Bot: Hi Cloud Counselage Intern, how can I help you ?")
    print("<------------------------------------------------------------------------------->")
    while True:
        usr = input("Cloud Counselage Intern: ")

        if usr.lower() == 'yes':
            print("Brtrix Chat Bot: Yes!")
            continue

        if usr.lower() == 'no':
            print("Brtrix Chat Bot: No?")
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
            print("Brtrix Chat Bot: It was good to be of help. I hope your all problems related to Internship is solved. All the best to you for your Internship!!!")
            break

        if usr == 'TOP5':
            TOP5 = True
            print("Will display 5 most relevent results now")
            continue


        t_usr = tfv.transform([cleanup(usr.strip().lower())])
        class_ = le.inverse_transform(model.predict(t_usr))[0]
        questionset = data[data['Class']==class_]

        if DEBUG:
            print("Question classified under category:", class_)
            print("{} Questions belong to this class".format(len(questionset)))

        cos_sims = []
        for question in questionset['Question']:
            sims = cosine_similarity(tfv.transform([question]), t_usr)
            cos_sims.append(sims)
            
        ind = cos_sims.index(max(cos_sims))

        if DEBUG:
            question = questionset["Question"][questionset.index[ind]]
            print("Assuming you asked: {}".format(question))

        if not TOP5:
            print("<------------------------------------------------------------------------------->")
            print("Brtrix Chat Bot:", data['Answer'][questionset.index[ind]])
        else:
            inds = get_max5(cos_sims)
            for ix in inds:
                print("Question: "+data['Question'][questionset.index[ix]])
                print("Answer: "+data['Answer'][questionset.index[ix]])
                print('-'*50)

        print("\n"*2)
        outcome = input("Was this answer helpful? Yes/No: ").lower().strip()
        if outcome == 'yes':
            cnt = 0
        elif outcome == 'no':
            inds = get_max5(cos_sims)
            print("<------------------------------------------------------------------------------->")
            sugg_choice = input("Brtrix Chat Bot: Do you want me to suggest you questions ? Yes/No: ").lower()
            if sugg_choice == 'yes':
                q_cnt = 1
                for ix in inds:
                    print(q_cnt,"Question: "+data['Question'][questionset.index[ix]])
                    # print("Answer: "+data['Answer'][questionset.index[ix]])
                    print('-'*50)
                    q_cnt += 1
                num = int(input("Please enter the question number you find most relevant: "))
                print("<------------------------------------------------------------------------------->")
                print("Brtrix Chat Bot: ", data['Answer'][questionset.index[inds[num-1]]])


chat()