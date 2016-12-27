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
import sys

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
        response = requests.get(url, headers={"Upgrade-Insecure-Requests":"1", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
        if not response.status_code / 100 == 2:
            print("Error: Unexpected http response {}".format(response))
            return None     
    
    except requests.exceptions.RequestException as e:
        print("Error {} in making request to url {} ".format(e,url))
        return None
        
    return response.text
    
    
def addToMongoDB(mongoClient, url, companyName, companyType, quarter, time, introList, questionList, answerList, summaryList):
        
    documentMap = {}
    documentMap['URL'] = url
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
        
    mongoClient.close()
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
    return addToMongoDB(mongoClient, url, companyName.text, companyType, Quarter.string, Time.string, IntroList, QuestionList, AnswerList, SummaryList)
    
'''
printUsage = False
if len(sys.argv) != 3:
    print("No. of arguments are not sufficient. ")
    printUsage = True
else:
    URL = sys.argv[1]
    companyType = sys.argv[2]
    if populateTranscriptFromSeekingAlpha(URL, companyType) == True:
        print("Document added successfully")
    else:
        print("Failed to add the document")

if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-help"):
    printUsage = True
    
if printUsage:
    print("How to Use: ")
    print("python FinTranscript.py <seekingalpha URL> <self|competitor|customer|supplier)")
'''