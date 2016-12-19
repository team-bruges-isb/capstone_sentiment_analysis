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
import json

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
            print("Error: Unexpected http response {}".format(response))
            return None     
    
    except requests.exceptions.RequestException as e:
        print("Error {} in making request to url {} ".format(e,url))
        return None
        
    return response.text
    
    
def addToMongoDB(mongoClient, companyName, companyType, quarter, time, introList, questionList, answerList, summaryList):
        
    documentMap = {}
    documentMap['companyName'] = companyName
    documentMap['quarter'] = quarter
    documentMap['time'] = time
    documentMap['companyType'] = companyType
    documentMap['sections'] = []
    
    introMap = {}
    introMap["id"] = "introduction"
    introMap["text"] = " ".join(introList)
    documentMap['sections'].append(introMap)
    
    for question in questionList:
        questionMap = {}
        questionMap["id"] = "question"
        questionMap["text"] = question
        documentMap['sections'].append(questionMap)
        
    for answer in answerList:
        answerMap = {}
        answerMap["id"] = "answer"
        answerMap["text"] = answer
        documentMap['sections'].append(answerMap)
    
    summaryMap = {}
    summaryMap["id"] = "summary"
    summaryMap["text"] = " ".join(summaryList)
    documentMap['sections'].append(summaryMap)

    retValue = True
    
    #jsonData = json.dumps(documentMap)
    #print(jsonData)
    
    try:
        db = mongoClient.documents
        result = db.transcripts.insert_one(documentMap)
        if result != None:
            print("Added Document with Object ID : " + str(result.inserted_id))
        else:
            retValue = False
            print("Failed to add Document")
    except Exception as e:
        print("Failed to add Document to mongodb, some expcetion occcured in insertion.")
        
    return retValue
    
    
def populateTranscriptFromSeekingAlpha(url, companyType):
    
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
    summaryString = ""
    questionStarted = False
    answerStarted = False
    introStarted = False
    introEnded = False
    summaryStarted = False
    IntroList = []
    QuestionList = []
    AnswerList = []
    SummaryList = []
    
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
            elif introStarted == True:
                IntroList.append(ptagList[index].text)
                continue
            elif summaryStarted == True:
                summaryString += str(ptagList[index].text)
                continue

        else:
            if answerString != "":
                AnswerList.append(answerString)
                SummaryList.clear()
                answerString = ""
                answerStarted = False
                questionStarted = False
                
            if summaryString != "":
                SummaryList.append(summaryString)
                summaryString = ""
                summaryStarted = False
        
            if str(ptagList[index]).find("\"question\"") != -1:
                questionStarted = True
                answerStarted = False  
            elif str(ptagList[index]).find("\"answer\"") != -1:
                answerStarted = True
                questionStarted = False
            elif str(ptagList[index]).find("Question-and-Answer Session") != -1:
                introStarted = False
                introEnded = True
            elif str(ptagList[index]).find("Operator") != -1 and introEnded == False:
                introStarted = True
            elif introEnded == True:
                summaryStarted = True
                
    print(len(QuestionList))
    print(len(AnswerList))
    print(len(IntroList))
    
    #print(" ".join(IntroList))
    
    #for question in QuestionList:
     #   print(question)
        
    #for answer in AnswerList:
    #    print(answer)
        
    #print(" ".join(SummaryList))
    
    #push toMongoDB
    return addToMongoDB(mongoClient, companyName.text, companyType, Quarter.string, Time.string, IntroList, QuestionList, AnswerList, SummaryList)
    

populateTranscriptFromSeekingAlpha('http://seekingalpha.com/article/4030878-adobe-systems-adbe-ceo-shantanu-narayen-q4-2016-results-earnings-call-transcript?part=single', 
                                   "competitor")
    