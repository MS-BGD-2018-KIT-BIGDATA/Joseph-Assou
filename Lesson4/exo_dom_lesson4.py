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
import time
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool
import asyncio
import aiohttp
import sys
sys.path.insert(0, '/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Wallet')
import walletstore as w


contributorname = []
contributorrating = []
contributororigin = []



def TopContributorsByCrawling():
    
    url = "https://gist.github.com/paulmillr/2657075"
    res = requests.get(url, auth=HTTPBasicAuth(w.user, w.Passwd))
    soup = BeautifulSoup(res.text, 'html.parser')
    listContributors = soup.find_all("tr")
   
    for i in range(1,257):
        contributorname.append(listContributors[i].find_all("td")[0].find("a").
                               text)
        contributorrating.append(int(listContributors[i].find_all("td")[1].
                                     text))
        contributororigin.append(listContributors[i].find_all("td")[2].text)
        
   
    #global df = df1.copy()
    return contributorname
    

def main():
    #Parallelize code
    
    TopContributorsByCrawling()
    print(contributorname)
    OwnRating=[]
    AsyncRes = []
    AsyncRes2 = []
    AsyncRes3 = []
#    if __name__ == '__main__':
#        start1 = time.time()        
#        with Pool() as p:
#            OwnRating=p.map(GetdataForParalelizationsynch, contributorname)
#    exectime1 = time.time()-start1
#    print("\nTemps execution multiprocess synchrone est", exectime1)
#    df1 = pd.DataFrame({'Name': contributorname,'Rating': contributorrating,
#                       'Origin': contributororigin, 'OwnRating': OwnRating})
#    time.sleep(2)
    start2= time.time()
    AsyncRes = GetdataForParalelizationAsynch(contributorname[0:100:1])
    time.sleep(0.5)
    AsyncRes2 = GetdataForParalelizationAsynch(contributorname[100:200:1])
    time.sleep(0.5)
    AsyncRes3 = GetdataForParalelizationAsynch(contributorname[200::1])
    exectime2=time.time()-start2
    print("\nTemps execution  asynchrone est", exectime2)
    print("1st list is \n :", AsyncRes)
    print("2nd list is \n :", AsyncRes2)
    print("3rd list is \n :", AsyncRes3)
    AsyncRes.extend(AsyncRes2)
    AsyncRes.extend(AsyncRes3)
    print(len(AsyncRes))
    df2 = pd.DataFrame({'Name': contributorname,'Rating': contributorrating,
                       'Origin': contributororigin, 'OwnRating': AsyncRes})
  
    
#    df1.set_index("OwnRating")
    df2.sort_values("OwnRating")
    print(df2)
    
def GetData(username):
    print(username + "\n")
    url = "https://api.github.com/users/"+username+"/repos"
    res = requests.get(url, auth=HTTPBasicAuth(w.user, w.Passwd))
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
    
def GetUrlFromContributor(contributorname):
    OwnRating1=[]
    for username in contributorname:
        OwnRating1.append(AvgRatingByTopContributorRepo(GetData(username)))
    print(OwnRating1) 
    return OwnRating1


def GetdataForParalelizationAsynch(username):
    urls=[]
    AsyncRes=[]
    for u in username:
        url = "https://api.github.com/users/"+u+"/repos"
        print(url)
        urls.append(url)
    futures = [call_url(url) for url in urls]    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    caca,_ = loop.run_until_complete(asyncio.wait(futures))
#    print("caca is \n", caca)
#    print("caca,_ is \n", caca,_)
    for fut in caca:
        AsyncRes.append(format(fut.result()))
    loop.close()
    return AsyncRes;
    


def GetdataForParalelizationsynch(username):
   
    url = "https://api.github.com/users/"+username+"/repos"
    mean = call_urlsynch(url)
    return mean
    
def GetMeanForUser(data):
    RepoRatingList = []
    RepoRatingList = list(map(lambda x:float(x['stargazers_count']), data))
    if len(RepoRatingList) > 0: 
        RepoRatingArray = np.array(RepoRatingList)
        usermean = np.mean(RepoRatingArray)
    else:
        usermean= 0
    return usermean
def call_urlsynch(url):

    res =requests.get(url, auth=HTTPBasicAuth(w.user, w.Passwd))
    if(res.status_code == 200):
        print('ok')
        data = js.loads(res.text)
    else:
        print("On vient de se faire dégager")
    mean = GetMeanForUser(data)
    return mean

async def call_url(url):

    res = await aiohttp.get(url,auth=aiohttp.BasicAuth(w.user, w.Passwd))
    data = await res.text()
    if(res.status == 200):
        d = js.loads(str(data))
    else:
        print("On vient de se faire dégager")
    mean = GetMeanForUser(d)
    return mean
    
    
main()
