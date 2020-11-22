from vgg import *
preds = []
preds = test(pic)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import csv
from itertools import chain 
import pandas as pd
from datetime import datetime

tokenizer = Tokenizer(num_words=1000, oov_token='<UNK>')
tokenizer.fit_on_texts(preds)

# Get our training data word index
word_index = tokenizer.word_index

def preprocess(text):  
  sequences = tokenizer.texts_to_sequences(text)
  return sequences


fields = ['id', 'w1','w2','w3','w4','w5','w6','w7','w8','w9','w10','time','camera'] 
filename = "captions.csv"
timimg = []
keywords = ["a black beard"]

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
timing.append(current_time)

with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  

        
    # writing the data rows  
    csvwriter.writerows(preprocess(preds))

df = pd.read_csv("captions.csv")
df = df.assign(time = timing)
df['camera']=1

def test_preprocess(test_text):
  search = preprocess(test_text)
  search = list(chain.from_iterable(search))
  return search

from collections import Counter   
def checkInFirst(a, b): 
     #getting count 
    count_a = Counter(a) 
    count_b = Counter(b) 
  
    #checking if element exsists in second list 
    for key in count_b: 
        if key not in  count_a: 
            return False
        if count_b[key] > count_a[key]: 
            return False
    return True
  
#Calling function 
def generate(df):
  for i in df.index:
    res = checkInFirst(df.iloc[i], test_preprocess(keywords))
    if res == True:
      return df.loc[i:i, ['time', 'camera']]