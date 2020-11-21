import ast
import numpy as np

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.image import img_to_array, load_img
from keras.models import Model
from keras.layers import Dense, LSTM, Dropout, Embedding
from keras.layers import Input
from keras.layers.merge import add
from keras.applications.vgg16 import VGG16, preprocess_input


file = open("models/vgg/wordtoix.txt", "r")
contents = file. read()
wordtoix = ast. literal_eval(contents)
file. close()
#print(type(wordtoix))

file = open("models/vgg/ixtoword.txt", "r")
contents = file. read()
ixtoword = ast. literal_eval(contents)
file. close()
#print(type(ixtoword))

base_model = VGG16(weights = 'imagenet')
base_model = Model(base_model.input, base_model.layers[-2].output)



def preprocess_img(img_path):
    #vgg16 excepts img in 224*224
    img = load_img(img_path, target_size = (224, 224))
    x = img_to_array(img)
    # Add one more dimension
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x)
    return x

def encode(image):
    image = preprocess_img(image)
    vec = base_model.predict(image)
    vec = np.reshape(vec, (vec.shape[1]))
    return vec.reshape(1,4096)


ip1 = Input(shape = (4096, ))
fe1 = Dropout(0.2)(ip1)
fe2 = Dense(256, activation = 'relu')(fe1)
ip2 = Input(shape = (34, ))
se1 = Embedding(1652, 200, mask_zero = True)(ip2)
se2 = Dropout(0.2)(se1)
se3 = LSTM(256)(se2)
decoder1 = add([fe2, se3])
decoder2 = Dense(256, activation = 'relu')(decoder1)
outputs = Dense(1652, activation = 'softmax')(decoder2)
model = Model(inputs = [ip1, ip2], outputs = outputs)

model.load_weights('models/vgg/image-caption-weights8.h5')

def greedy_search(pic):
    max_length = 34
    start = 'startseq'
    for i in range(max_length):
        seq = [wordtoix[word] for word in start.split() if word in wordtoix]
        seq = pad_sequences([seq], maxlen = max_length)
        yhat = model.predict([pic, seq])
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        start += ' ' + word
        if word == 'endseq':
            break
    final = start.split()
    final = final[1:-1]
    return final

#greedy_search(img)

def test(img):
  img = encode(img)
  return greedy_search(img)