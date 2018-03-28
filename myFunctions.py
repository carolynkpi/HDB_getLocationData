#Import Libraries
import pandas as pd
import requests
import json as json
import time
import csv
import pandas as pd
import requests
import json as json
import time
import csv

'''
tryGET: Function to keep trying a GET request, handling the following errors: 
1. Request function error
2. Request returned error
3. Google API's returned error 

-Inputs-
maxTries <int> : Number of tries to attempt before recording a failure. 
reqURL <char> : Request URL
progress <bool> : Indicator for whether to display number of tries attempted. 
sleep <int> : Number of seconds to sleep after each error (except request function error, which will sleep for 10 seconds by default). 

-Returns-
reqStatus <int> : Request's returned status code. Every number except 200 is an error. 
returnedStatus <char> : Google API's returned status code. Every value except 'OK' is an error. 
data <dict> : Request's returned text in json dictionary format. 
tries <int> : Number of tries attepted.  

'''
def tryGET(maxTries, reqURL, progress = True, sleep = 5):
    reqStatus = -1
    returnedStatus = ''
    tries = 0
    while tries < maxTries: # monitor number of successful requests made. 
        try:
            req = requests.get(reqURL)
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(10)   
            continue # try indefinitely every 10 seconds until request is successful.
            
        if progress:
            print('Try: %i. ' %(tries+1))
        
        time.sleep(sleep)
        tries +=1
        reqStatus = req.status_code
        if reqStatus != 200:  
            continue # try again if the successful request's returned status is not 200.
        else: 
            data = json.loads(req.text)
            returnedStatus = data['status']
            if returnedStatus != 'OK': 
                continue # try again if Google's returned status is not 'OK'.
            else:
                break
    return reqStatus, returnedStatus, data, tries

'''
tryGETp: Similar to tryGET function, but incorporates a tracker for Google Places API (placesTracker() from placestracker.py). 

-Inputs-
maxTries <int> : Number of tries to attempt before recording a failure. 
reqURL <char> : Request URL
progress <bool> : Indicator for whether to display number of tries attempted. 
sleep <int> : Number of seconds to sleep after each error (except request function error, which will sleep for 10 seconds by default). 

-Returns-
reqStatus <int> : Request's returned status code. Every number except 200 is an error. 
returnedStatus <char> : Google API's returned status code. Every value except 'OK' is an error. 
data <dict> : Request's returned text in json dictionary format. 
tries <int> : Number of tries attepted.  

'''
from placesTracker import *
def tryGETp(maxTries, reqURL, progress = True, sleep = 5):
    reqStatus = -1
    returnedStatus = ''
    tries = 0
    while tries < maxTries: # monitor number of successful requests made.
        
        if placesTracker():
            try:
                req = requests.get(reqURL)
            except requests.exceptions.RequestException as e:
                print(e)
                time.sleep(10)
                continue # try indefinitely every 10 seconds until request is successful.
            
            if progress:
                print('Try: %i. ' %(tries+1))
        
            time.sleep(sleep)
            tries +=1
            reqStatus = req.status_code
            if reqStatus != 200: 
                continue # try again if the successful request's returned status is not 200.
            else: 
                data = json.loads(req.text)
                returnedStatus = data['status']
                if returnedStatus != 'OK':
                    continue # try again if Google's returned status is not 'OK'.
                else:
                    break
        else: 
            return 999, 'Place Tracker Query Exceeded', {}, tries
    return reqStatus, returnedStatus, data, tries

'''
getParamString: Function to create a parameter string for the request URL given a dictionary of parameters. 

-Inputs-
params <dict> : A dictionary with keys being API parameter names and values being the corresponding value. 

-Returns-
paramString <char> : A concatenated string of parameter names and values, to be appended to the API request URL. 

'''
def getParamString(params):
    paramString = ''
    for k, v  in params.items():
        if paramString == '':
            paramString = k + '=' + v
        else:
            paramString = paramString + '&' + k + '=' + v
    return paramString

'''
getKeys: Function to read API keys from a key file. 
 -Note: Each Google API requires a separate API key. I stored all the keys in a single file, which will be read below. 
 -Warning: Do not reveal your key in your codes! The API keys are tied to the API usage limits and billing!
 
-Inputs-
keyFile <char> : Name of the file containing the keys. 
                 -------Sample of a key file------------------------------------------
                        GoogleMapsDistanceMatrix: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                        GoogleMapsGeocoding: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                        GooglePlaces: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                 ---------------------------------------------------------------------
-Returns-
keys <dict> : A dictionary of keys with the key being the name of th Google API as shown above and the value being the corresponding Google API key. 

'''
def getKeys(keyFile):
    f = open(keyFile)
    lines = f.readlines()
    f.close()
    keys = {}
    for l in lines:
        k,v = l[:-1].split(':')
        keys[k] = v
    return keys