import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) 
#nltk.download('punkt') # use only at starting
#nltk.download('wordnet') # use only at starting

f=open('chatbot_faq.txt','r',errors = 'ignore')
raw=f.read()
raw = raw.lower()# converts to lowercase

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
word_tokens = nltk.word_tokenize(raw)# converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hi", "hello","greetings", 'hii', 'Hie',"what's up","hey")
GREETING_RESPONSES = ["hi", "hey", "hi there", 'Hie',"hello", "I am Happy to talk with you!"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am not understanding what you are saying!"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

flag=True
print("=================================== FAQ_BOT ===================================")
print("FAQ_BOT =>  Hey i am a chatbot. I will answer your queries about Cloud Counselage's IP.")
print("----------------------------------------------------------------------------------")
print("If you want to exit, type Bye!")
print("----------------------------------------------------------------------------------")
print()
while(flag==True):
    user_response = input("User => ")
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("FAQ_BOT =>  You are welcome..")
            print("----------------------------------------------------------------------------------")
        else:
            if(greeting(user_response)!=None):
                print("FAQ_BOT =>  "+greeting(user_response))
                print()
            else:
                print("FAQ_BOT =>  ",end="")
                print(response(user_response))
                print()
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("----------------------------------------------------------------------------------")
        print("FAQ_BOT =>  Bye! Visit again for any queries..")
        print("==================================================================================")
