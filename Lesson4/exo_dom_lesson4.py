#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 12:08:49 2017

@author: joseph
"""

import urllib
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
import functools as ft
import pandas as pd
import json as js
import threading
import time
import threading
import time
from requests.auth import HTTPBasicAuth

Token = "c4042386894ab260821a0b55fe0f99fdbe65acc3"
user = "RavimoShark"

def TopContributorsByCrawling():
    
    url = "https://gist.github.com/paulmillr/2657075"
    res = requests.get(url, auth=HTTPBasicAuth(user, Token))
    soup = BeautifulSoup(res.text, 'html.parser')
    listContributors = soup.find_all("tr")
    contributorname = []
    contributorrating = []
    contributororigin = []

    
    for i in range(1,257):
        contributorname.append(listContributors[i].find_all("td")[0].find("a").
                               text)
        contributorrating.append(int(listContributors[i].find_all("td")[1].
                                     text))
        contributororigin.append(listContributors[i].find_all("td")[2].text)
        
    
    
    df = pd.DataFrame({'Name': contributorname,'Rating': contributorrating,
                       'Origin': contributororigin})
    return df
    

def main():
    
    GetUrlFromContributor(TopContributorsByCrawling())
    #print(AvgRatingByTopContributorRepo(GetData("GrahamCampbell")))
    
def GetData(username):
    print(username + "\n")
    url = "https://api.github.com/users/"+username[0]+"/repos"
    res = requests.get(url, auth=HTTPBasicAuth(user, Token))
    if(res.ok):
         data = js.loads(res.text or res.content)
    else:
        print("On vient de se faire dégager")
    return data
     
def AvgRatingByTopContributorRepo(data):
    
    RepoRatingList = [] 
    RepoRatingList = list(map(lambda x:float(x['stargazers_count']), data))
    if len(RepoRatingList) > 0: 
        RepoRatingArray = np.array(RepoRatingList)
        return np.mean(RepoRatingArray)
    else:
        return 0
    
def GetUrlFromContributor(df):
    OwnRarting=[]
    for username in zip(df.Name):
        OwnRarting.append(AvgRatingByTopContributorRepo(GetData(username[0])))
    dfmeanrating = pd.DataFrame({'OwnRating': OwnRarting})
    print(OwnRarting)
    dfFinal = pd.concat(df, dfmeanrating) 
    print (dfFinal)
    return dfFinal

main()


class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      # Get lock to synchronize threads
      threadLock.acquire()
      print_time(self.name, self.counter, 3)
      # Free lock to release next thread
      threadLock.release()

   def print_time(threadName, delay, counter):
      while counter:
          time.sleep(delay)
          print ("%s: %s" % (threadName, time.ctime(time.time())))
          counter -= 1

#threadLock = threading.Lock()
#threads = []
#
## Create new threads
#thread1 = myThread(1, "Thread-1", 1)
#thread2 = myThread(2, "Thread-2", 2)
#
## Start new Threads
#thread1.start()
#thread2.start()
#
## Add threads to thread list
#threads.append(thread1)
#threads.append(thread2)
#
## Wait for all threads to complete
#for t in threads:
#   t.join()
#print ("Exiting Main Thread")