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
import asyncio
import aiohttp

citysource=''
api_key = 'AIzaSyCX-JieImQLw7SqnvP60nYUVAJuhkJqGoE'
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
    Datframe()

def callAPI(city):
    orig = citysource
    dest = city
    print(dest)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+orig+"&destinations="+dest+"&mode=driving&  units=imperial&key="+api_key
    print(url)
    res = requests.get(url)
    if(res.ok):
         data = js.loads(res.text or res.content)
    else:
        print("On vient de se faire dégager")
    dist = data["rows"][0]["elements"][0]["distance"]["value"]
    print (float(dist))
    return float(dist)

def Datframe():
    CityDistance = np.arange(100*100).reshape(100,100)
    CityD=[]
    i=0
    
    for c in contributorname:
        global citysource 
        citysource = c
        with Pool() as p:
            CityD = p.map(callAPI, contributorname)
            CityDistance[i] = np.array(CityD)
        i+=1     
    print(CityDistance)
    return CityDistance

main()