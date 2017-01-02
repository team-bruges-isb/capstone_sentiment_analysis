# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 21:24:42 2016

@author: Shark
"""
#import statements
import json
import bson
import collections, re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer 
import nltk
from xlrd import open_workbook
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

#Read MongoDB Data file 
def readBsonData(): 
    import bson
    with open('C:/Users/Shark/Desktop/Capstone/Data/transcripts.bson','rb') as f:
        data = bson.decode_all(f.read())    
        Docid = list(range(len(data)))
        dataPrep(data)
        iter = 0
        split_text = []
        for row in data:
            section = row
            print(len(row))
            print(section.keys())
            print(len(section['sections']))
            #print(sections[32]['id'])
            #print(sections[32]['text'])
            split_text = split_cleanText(section)
            bagofwords = [ collections.Counter(re.findall(r'\w+', txt)) for txt in split_text]
            sumbags = sum(bagofwords, collections.Counter())
            #createTFIDF(iter, section)
            iter = iter + 1
            break

def dataPrep(data):
    df = pd.DataFrame(columns=('docid','quarter', 'companyName', 'companyType','text' ))
    iter = 0
    for row in data:
        print(len(row['sections']))
        for iter in range(len(row['sections'])):
            text_iter = row['sections']
            text_full ="".join(text_iter[iter]['text'])
            #print(text_full)
    
def split_cleanText(section): 
    companyNames = section['companyName']
    companyType = section['companyType']
    time = section['time']
    quarter = section['quarter']
    sections = section['sections']
    #print(sections.keys())
    URL = section['URL']
    punctuation_pattern = ' |\.$|\. |, |\/|\(|\)|\'|\"|\!|\?|\+'
    #str_replace = lambda str: str.replace('<', '').replace('>', '').replace('/', '').replace('\-','')
    #sections[32]['text'] = sections[32]['text'].apply(str_replace)
    ltext = sections[32]['text'].lower()
    forbidden_words = set(stopwords.words('english'))
    #wtext = [w for w in re.split(punctuation_pattern, ltext)]
    wtext = [w for w in re.split(punctuation_pattern, ltext) if w not in forbidden_words]
    return wtext
    #word_counts = count_transformer.fit_transform(ltext)
    #print(word_counts)
    
def createTFIDF(DocId, section):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(section)
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
        
def readMcDonaldData(): 
    McD_Dictionary = open_workbook('C:/Users/Shark/Desktop/Capstone/Data/LoughranMcDonald_MasterDictionary_2014.xlsx') 
    for s in McD_Dictionary.sheets():
        print('Sheet:',s.name)
         #print 'Sheet:',s.name
        values = []
        headers = [str(cell.value) for cell in s.row(0)]
        print(headers) 
         
    
readBsonData()