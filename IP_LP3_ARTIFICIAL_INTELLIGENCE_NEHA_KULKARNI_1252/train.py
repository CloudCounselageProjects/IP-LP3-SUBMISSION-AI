# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:38:17 2020

@author: Admin
"""

import pandas as pd

import pickle
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
import nltk
from nltk.stem.lancaster import LancasterStemmer
#cleans the word that means if the word is saying it will return say
stemmer=LancasterStemmer()
def cleanup(sentence):
    word_tok=nltk.word_tokenize(sentence)
    stemmed_words=[stemmer.stem(w) for w in word_tok]
    return "".join(stemmed_words)

le=LE()
#Convert a collection of raw documents to a matrix of TF-IDF features.
#to count the stop words,  cut-off in the literature, basically are ignored
tfv=TfidfVectorizer(min_df=1,stop_words='english')

data=pd.read_csv("qna.csv")
#data.keys()
questions=data['questions'].values
X=[]
#Cleansing Questions
for question in questions:
    #print(question)
    X.append(cleanup(question))

#fitting into tfv
X=tfv.fit_transform(X)

#Labelling Categorical Data(the classes in y)
Y=le.fit_transform(data['classes'])

#splitting dataset into train and test
train_x, test_x, train_y, test_y=tts(X,Y, test_size=0.2)

#support vector machine
model=SVC(kernel="linear")
model.fit(train_x,train_y)

print(model.score(test_x,test_y))


#
f = open("cc_bot.pickle",'wb+')
pickle.dump(model,f)
f.close()


#
#
