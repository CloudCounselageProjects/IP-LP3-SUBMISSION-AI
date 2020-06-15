#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle


# In[2]:


import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import matplotlib.pyplot as plt


# In[3]:


import tensorflow as tf


# In[4]:


words=[]
classes = []
documents = []
ignore_words = ['?', '!','.']
data_file = open('intents.json').read()
intents = json.loads(data_file)


# In[5]:


for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


# In[6]:


words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

print (len(documents), "documents")


# In[7]:


classes = sorted(list(set(classes)))
print (len(classes), "classes", classes)
print (len(words), "unique lemmatized words", words)


# In[8]:


pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))


# In[9]:


training = []
output_empty = [0] * len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])


# In[10]:


random.shuffle(training)
training = np.array(training)
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")


# In[11]:


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('accuracy')>0.90 and logs.get('loss')<0.40):
            print("\nReached 90% accuracy so cancelling training!")
            self.model.stop_training = True

callbacks = myCallback()
model = Sequential()
model.add(Dense(132, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(38, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))


# In[12]:


model.summary()


# In[13]:


sgd = SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


# In[14]:


hist = model.fit(np.array(train_x), np.array(train_y), epochs=1500, batch_size=5, verbose=1,callbacks=[callbacks])
model.save('chatbot.h5', hist)

print("model created")


# In[15]:

"""
plt.plot(hist.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()
"""

# In[16]:


from keras.models import load_model
model = load_model('chatbot.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


# In[17]:


def clean_up_sentence(sentence):
    sent_words = nltk.word_tokenize(sentence)
    sent_words = [lemmatizer.lemmatize(word.lower()) for word in sent_words]
    return sent_words


# In[18]:


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


# In[19]:


def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.30
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


# In[20]:


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


# In[66]:


flag=True
resp = []
while(flag==True):
    try:
        res = input('You: ')
        if res=="quit" or res=="stop" or res=='Quit' or res=="Stop":
            flag=False
            print("Bot: Okay")
        else:
            print('Bot:',chatbot_response(res))
    except Exception:
        print("Bot: Sorry I can't understand")


# In[ ]:





# In[ ]:




