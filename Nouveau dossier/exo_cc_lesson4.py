#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:33:10 2017

@author: joseph
"""

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
sys.path.insert(0, '/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Wallet')
import walletstore as w
import asyncio
import aiohttp

citysource=''
contributorname=[]

def TopCity():
    
    url = "https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peuplées"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    listContributors = soup.find_all("tr")
   
    
    for i in range(1,101):
        contributorname.append(listContributors[i].find_all("td")[1].find("a").
                               text)
 
    #global df = df1.copy()
    return contributorname

def main():
    print(len(TopCity()))
    Dataframe()

def callAPI(city):
    orig = citysource
    dest = city
    print(dest)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+orig+"&destinations="+dest+"&mode=driving&  units=imperial&key="+w.api_key
    res = requests.get(url)
    if(res.ok):
         data = js.loads(res.text or res.content)
    else:
        print("On vient de se faire dégager")
        
    dist = data["rows"][0]["elements"][0]["distance"]["value"]
    
    if data['status'] == 'OVER_QUERY_LIMIT' :
        return 0
    else:
        print(float(dist))
        return float(dist)
        

def Dataframe():
    CityDistance = np.arange(100*100).reshape(100,100)
    CityTest = np.arange(9).reshape(3,3)
    CityD = []
    i=0
    
    for c in contributorname:
        global citysource 
        citysource = c
        with Pool() as p:
            CityD = p.map(callAPI, contributorname))
            CityDistance[i] = np.asarray(CityD)
            i =+ 1
    df = pd.DataFrame(CityDistance, columns=contributorname)
    df.to_csv()
    
    
    #print(CityTest)
    #return CityDistance

main()