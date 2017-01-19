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
cur = db.transcripts.find({"companyName": "Flextronics International Ltd. (NASDAQ:FLEX)"})

mystop = STOPWORDS
with open('C:\\Users\\rahulgup\\Desktop\\ISB\\Capstone\\capstone_sentiment_analysis\\metadata\\Stopwords.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        mystop.add(row[0])
        mystop.add(row[0].lower())

mystop.add('business')
mystop.add('continue')
mystop.add('remain')



donalddict = pandas.read_excel("C:\\Users\\rahulgup\\Desktop\\ISB\\Capstone\\capstone_sentiment_analysis\\metadata\\LoughranMcDonald_MasterDictionary_2014.xlsx")
donaldSet = set()
for x in donalddict['Word'].values:
    donaldSet.add(str(x).lower())


        
cur = db.transcripts.find({"companyName": "Flextronics International Ltd. (NASDAQ:FLEX)"})        
for obj in cur:
    mytext = (obj['sections'][0]['text'])
    reducedText = ''
    for word in mytext.split():
        if word.lower() in donaldSet:
            reducedText = reducedText + ' ' + word
    
    quarter = (obj['quarter'])
    print(quarter)
    wordCloud = WordCloud(stopwords = mystop, scale = 2, max_words = 50).generate(reducedText)
    plt.imshow(wordCloud)
    break

import dateutil
from dateutil import parser
def mydatehandler(datestring):
    datestring = ' '.join(datestring.split())
    dt = parser.parse(datestring)
    return dt.strftime("%m/%d/%Y")


    