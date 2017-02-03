# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:08:49 2017

@author: rahulgup
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from wordcloud import STOPWORDS, WordCloud
import csv
import matplotlib.pyplot as plt
import pandas
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

def connectToLocalMongoDB():
    mongoClient = MongoClient()
    
    try:
        # The ismaster command is cheap and does not require auth.
        mongoClient.admin.command('ismaster')
        return mongoClient
        
    except ConnectionFailure:
        print("MongoDB Server not available")
        return None
        
mongoDB = connectToLocalMongoDB()
db = mongoDB.documents        
#cur = db.transcripts.find({"companyName": "Flextronics International Ltd. (NASDAQ:FLEX)"})
cur = db.transcripts.find({"companyName": {'$regex': 'Plexus Corp', '$options' : 'i'}})

mystop = STOPWORDS
with open('C:\\Users\\rahulgup\\Desktop\\ISB\\Capstone\\capstone_sentiment_analysis\\metadata\\Stopwords.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[0])
        mystop.add(row[0])
        mystop.add(row[0].lower())

mystop.add('business')
mystop.add('continue')
mystop.add('remain')
mystop.add('thank')
mystop.add('think')
mystop.add('look')
mystop.add('say')
mystop.add('call')
mystop.add('end')
mystop.add('customer')
mystop.add('really')
mystop.add('fiscal')
mystop.add('program')
mystop.add('result')
mystop.add('market')
mystop.add('Please')
mystop.add('going')
mystop.add('looking')


donalddict = pandas.read_excel("C:\\Users\\rahulgup\\Desktop\\ISB\\Capstone\\capstone_sentiment_analysis\\metadata\\LoughranMcDonald_MasterDictionary_2014.xlsx")
donaldSet = set()
for x in donalddict['Word'].values:
    donaldSet.add(str(x).lower())


cur = db.transcripts.find({"companyName": "Flextronics International Ltd. (NASDAQ:FLEX)"})        

cur = db.transcripts.find({"companyName": {'$regex': 'Box', '$options' : 'i'}})
     
for obj in cur:
    mytext = '' 
    mystext = (obj['sections'][0]['text'])
    for index in range(len(obj['sections'])):
        mytext = mytext + ' ' + obj['sections'][index]['text']
    quarter = (obj['quarter'])
    companyName = obj['companyName']
    print(quarter)
    break;

    reducedText = ''
    for word in mytext.split():
        if word.lower() in donaldSet:
            reducedText = reducedText + ' ' + word
    
    quarter = (obj['quarter'])
    companyName = obj['companyName']
    print(quarter)
    wordCloud = WordCloud(stopwords = mystop, width = 600, height = 300, scale = 3, max_words = 25, background_color = "white").generate(reducedText)
    plt.imshow(wordCloud)
    plt.axis('off')
    mystring = ""
    mystring = companyName + '_' + quarter + '.jpg'
    mystring = mystring.replace(" ", "_")
    mystring = mystring.replace("(", "")
    mystring = mystring.replace(")", "")
    mystring = mystring.replace(":", "")
    mystring = mystring.replace("/", "")
    plt.savefig(mystring, bbox_inches='tight')
    plt.close()








tokens = mytext.split()
bigrams(tokens)


finalbigramlist = []
for bg in mybigramlist:
    if bg[0].lower() in mystop:
        continue
    if bg[1].lower() in mystop:
        continue
    finalbigramlist.append(bg)




token = nltk.word_tokenize(mytext)
bigrams = ngrams(token,2)


mylist = {}
fdist = nltk.FreqDist(bigrams)
for k,v in fdist.items():
    templist = list(k)
    if v in mylist:
        mylist[v].append(templist)
    else:
        mylist[v] = []
        mylist[v].append(templist)

finalList = {}
for key in mylist:
    for items in mylist[key]:    
        if items[0].lower() in mystop:
            continue
        if items[1].lower() in mystop:
            continue
        if key in finalList:
            finalList[key].append(items)
        else:
            finalList[key] = []
            finalList[key].append(items)

mylist = finalList
finalList = {}
for key in mylist:
    for items in mylist[key]:    
        if len(items[0]) == 1:
            continue
        if len(items[1]) == 1:
            continue
        if key in finalList:
            finalList[key].append(items)
        else:
            finalList[key] = []
            finalList[key].append(items)
            
for key in finalList:
    for items in finalList[key]:
        print(items[0], items[1], ",", key)
    

import dateutil
from dateutil import parser
def mydatehandler(datestring):
    datestring = ' '.join(datestring.split())
    dt = parser.parse(datestring)
    return dt.strftime("%m/%d/%Y")


    