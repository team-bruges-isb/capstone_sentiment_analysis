# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
#import statements
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from lxml import html
import requests

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
        
    tree = html.fromstring(response.content)
    return tree

    