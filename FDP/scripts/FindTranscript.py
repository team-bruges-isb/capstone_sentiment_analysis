# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 21:03:31 2016

@author: rahulgup
"""

from lxml import html
import requests
from bs4 import BeautifulSoup
import re
import sys
import csv
import subprocess


def getHtmlTreeFromURL(url):
    print(url)
    try:
        response = requests.get(url, headers={"Upgrade-Insecure-Requests":"1", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"})
        if not response.status_code / 100 == 2:
            print("Error: Unexpected http response {}".format(response))
            return None     
    
    except requests.exceptions.RequestException as e:
        print("Error {} in making request to url {} ".format(e,url))
        return None
        
    return response.text
    
def findTranscripts(csvFileWithSymbols):
    
    csvFile = open(csvFileWithSymbols, "r")
    reader = csv.reader(csvFile)
    for row in reader:
        companySymbol = row[0]
        companyType = row[2]

        print("")
        print("")
        print("")

        saUrl = "http://www.seekingalpha.com/symbol/" + companySymbol + "/earnings/transcripts"
        #subprocess.call(['C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', saUrl])
        htmlContent = getHtmlTreeFromURL(saUrl)
        if htmlContent == None:
            print("could not find transcripts for company: " + row[1] + row[0])
            continue
        
        soup = BeautifulSoup(htmlContent, "lxml")
        taglist = soup.find_all("div", class_="symbol_article")
        if len(taglist) == 0:
            print("could not find transcripts for company: " + row[1] + row[0])
            continue;

        for tag in taglist:
            if (tag.a["href"]).find("earning") != -1 and (tag.a["href"]).find("transcript") != -1: 
                print(tag.a["href"])
        
    csvFile.close()
    
csvFile = sys.argv[1]
findTranscripts(csvFile)
