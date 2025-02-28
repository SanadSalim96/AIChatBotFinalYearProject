import random, json
import pickle

import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('karakDatabase/intents.json').read())

# initlize three list 
words =  list()
documents = list()
classes = list()


# ignore chars in sentenses
ignoreChars = ['?', '!', ',', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        
        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignoreChars]
words = sorted(list(set(words))) # remove any duplication 
classes = sorted(set(classes))

pickle.dump(words, open('karakPickle/words.pkl', 'wb'))
pickle.dump(classes, open('karakPickle/classes.pkl', 'wb'))


training = list()
output_empty = [0]*len(classes)

for document in documents:
    bag = list()
    words_patterns = document[0]
    words_patterns = [lemmatizer.lemmatize(word.lower()) for word in words_patterns]
    for word in words:
        bag.append(1) if word in words_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(512, input_shape= (len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay = 1e-6, momentum=0.5, nesterov=True)

model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=5, verbose=1)
model.save('karakModel/chatbotmodel.h5', hist)
print('done!')
