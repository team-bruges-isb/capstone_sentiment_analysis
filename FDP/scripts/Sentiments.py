# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:32:56 2016

@author: rahulgup
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connectToLocalMongoDB():
    mongoClient = MongoClient()
    
    try:
        # The ismaster command is cheap and does not require auth.
        mongoClient.admin.command('ismaster')
        return mongoClient
        
    except ConnectionFailure:
        print("MongoDB Server not available")
        return None
        
