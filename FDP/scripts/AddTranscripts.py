# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 11:21:53 2016

@author: rahulgup
"""

from FinTranscript import *
import sys
import csv
import subprocess

def collectTranscripts():
    
    csvFileWithURLs = "C:\\Users\\rahulgup\\Desktop\\ISB\\capstone\\capstone_sentiment_analysis\\metadata\\sentimenturl.csv"
    
    csvFile = open(csvFileWithURLs, "r")
    reader = csv.reader(csvFile)
    failedList = []
    count = 0
    for row in reader:
        partialUrl = row[0]

        if partialUrl.find("earning") == -1 or partialUrl.find("transcript") == -1:
            continue

        count = count + 1
        completeUrl = "http://www.seekingalpha.com" + partialUrl + "?part=single"
        
        result = populateTranscriptFromSeekingAlpha(completeUrl, "competitor")
        if result == False:
            print("Failed to Add Url: " + completeUrl)
            failedList.append(completeUrl)
            
    csvFile.close()
    print("Total URL = ", count)
    print("failed URL = ", len(failedList))
        
