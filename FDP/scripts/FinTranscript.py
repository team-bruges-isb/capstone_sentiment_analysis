# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
#import statements
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from lxml import html
import requests

from bs4 import BeautifulSoup

import re

def connectToLocalMongoDB():
    mongoClient = MongoClient()
    
    try:
        # The ismaster command is cheap and does not require auth.
        mongoClient.admin.command('ismaster')
        return mongoClient
        
    except ConnectionFailure:
        print("MongoDB Server not available")
        return None
        
        

def getHtmlTreeFromURL(url):
    try:
        response = requests.get(url)
        if not response.status_code / 100 == 2:
            print("Error: Unexpected response {}".format(response))
            return None     
    
    except requests.exceptions.RequestException as e:
        print("Error {} in making request to url {} ".format(e,url))
        return None
        
    return response.text 
    
def populateTranscriptFromSeekingAlpha(url):
    
    mongoClient = connectToLocalMongoDB()
    if mongoClient == None:
        return False
        
    htmlContent = getHtmlTreeFromURL(url)
    if htmlContent == None:
        return False
        
    print("I have reached the soup preparation state")
    soup = BeautifulSoup(htmlContent, "lxml")
    
    #mytag = None
    #for tag in soup.find_all(itemprop="articleBody"):
        #mytag = tag
        
    ptagList = soup.find_all("p", class_=re.compile("p p*"))
    
    companyName = ptagList[0]
    Quarter = ptagList[1]
    Time = ptagList[2]

    print(companyName.text)
    print(Quarter.string)
    print(Time.string)

    print(len(ptagList))
    
    answerString = ""
    questionStarted = False;
    answerStarted = False;
    IntroList = []
    QuestionList = []
    AnswerList = []
    for index in range(3, len(ptagList)):
        
        isStrong = False
        if ptagList[index].strong != None:
            isStrong = True
            
        if isStrong == False:    
            if questionStarted == True:
                QuestionList.append(ptagList[index].text)
                questionStarted = False;
                continue
            elif answerStarted == True:
                answerString += str(ptagList[index].text)
                continue
            else:
                IntroList.append(ptagList[index].text)

        else:
            if answerString != "":
                AnswerList.append(answerString)
                answerString = ""
                answerStarted = False
                questionStarted = False
        
            if str(ptagList[index]).find("\"question\"") != -1:
                questionStarted = True
                answerStarted = False  
            elif str(ptagList[index]).find("\"answer\"") != -1:
                answerStarted = True
                questionStarted = False
                
    print(len(QuestionList))
    print(len(AnswerList))
    print(len(IntroList))
    
    
    
    print(IntroList)
    

populateTranscriptFromSeekingAlpha('http://seekingalpha.com/article/4016206-flex-flex-q2-2017-results-earnings-call-transcript?part=single')
    