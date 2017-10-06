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
    print(city)
    orig = city(0)
    dest = city(1)
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&  units=imperial&key="+api_key.format(str(orig),str(dest))
    res = requests.get(url)
    if(res.ok):
         data = js.loads(res.text or res.content)
    else:
        print("On vient de se faire dégager")
    dist = data["rows"][0]["elements"][0]["distance"]["value"]
    print (dist)

def Datframe():
    CityDistance = np.arange(100*100).reshape(100,100)
    i=0
    
    for c in contributorname:
        params=[(c,y) for y in contributorname]
        with Pool() as p:
            CityDistance[i]=p.map(callAPI, params)
        i += 1
    
    df = pd.DataFrame(CityDistance)
    print(df)


main()