# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 21:24:42 2016
Updated on Mon Jan 02 20:53:30 2017 
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
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

#Read MongoDB Data file 
def readBsonData(): 
    import bson
    with open('C:/Users/Shark/Desktop/Capstone/Data/transcripts.bson','rb') as f:
        data = bson.decode_all(f.read())    
        Docid = list(range(len(data)))
        transdf = dataPrep(data)
        #print(transdf.loc[0]['text'])
        split_text = split_cleanText(transdf.loc[0]['text'])
        createTFIDF(0, split_text)
        McDict = readMcDonaldData()
"""
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
"""

## Create Data frame from the Mongodata and padding a document ID 
def dataPrep(data):
    df = pd.DataFrame(columns=('docid','quarter', 'companyName', 'companyType','text' ))
    iter = 0
    for row in data:
        #print(len(row['sections']))
        for i in range(len(row['sections'])):
            text_iter = row['sections']
            text_full ="".join(text_iter[i]['text'])
        df.loc[iter] = [iter, row['quarter'], row['companyName'], row['companyType'], text_full]
        iter = iter+1
    return df 
        
            
#Word split from the text, convert all to Lower case and eliminate stop words     
def split_cleanText(section): 
    punctuation_pattern = ' |\.$|\. |, |\/|\(|\)|\'|\"|\!|\?|\+'
    ltext = section.lower()
    forbidden_words = set(stopwords.words('english'))
    wtext = [w for w in re.split(punctuation_pattern, ltext) if w not in forbidden_words]
    #print(wtext)
    return wtext
    #word_counts = count_transformer.fit_transform(ltext)
    #print(word_counts)

#Create Tf -IDF from the text     
def createTFIDF(DocId, section):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(section)
    tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
    X_train_tf = tf_transformer.transform(X_train_counts)
    #print(X_train_counts.shape)
    #print(X_train_tf)

# Read McDonald's Dictionary into Df        
def readMcDonaldData(): 
    McD_Dictionary = pd.ExcelFile('C:/Users/Shark/Desktop/Capstone/Data/LoughranMcDonald_MasterDictionary_2014.xlsx') 
    McDdf = pd.DataFrame(columns=('Word', 'Sequence Number', 'Word Count', 'Word Proportion', 'Average Proportion', 'Std Dev', 'Doc Count', 'Negative', 'Positive', 'Uncertainty', 'Litigious', 'Constraining', 'Superfluous', 'Interesting', 'Modal', 'Irr_Verb', 'Harvard_IV', 'Syllables', 'Source'))
    McDdf = McD_Dictionary.parse('LoughranMcDonald_MasterDictiona')
    return McDdf
    
         
    
readBsonData()