import nltk
import numpy as np
import random
import string

f = open('data.txt', errors = 'ignore')
data=f.read()
data=data.lower()
sentence_tokens = nltk.sent_tokenize(data)
word_tokens = nltk.word_tokenize(data)
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello"]
def greeting(sentence):
     for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def response(user_response):
    Joe_response='sent'
    sentence_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sentence_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        Joe_response=Joe_response+"I am sorry! I don't understand you"
        return Joe_response
    else:
        Joe_response = Joe_response+sentence_tokens[idx + 1]
        return Joe_response
flag=True
print("Joe: My name is Joe. I will answer any queries you have regarding the internship program. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("Joe: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("Joe: "+greeting(user_response))
            else:
                print("Joe: ",end="")
                print(response(user_response))
                sentence_tokens.remove(user_response)
    else:
        flag=False
        print("Joe: Bye! take care..")