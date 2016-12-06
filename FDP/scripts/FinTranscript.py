# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import statements
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from lxml import html
import requests

#global mongoClient Object
mongoClient = None


def connectToLocalMongoDB():
    mongoClient = MongoClient()
    
    try:
        # The ismaster command is cheap and does not require auth.
        mongoClient.admin.command('ismaster')
        return true
        
    except ConnectionFailure:
        print("Server not available")
        return False
        
        

def getHtmlTreeFromURL(url):
    page = requests.get(url)
    
        
    
