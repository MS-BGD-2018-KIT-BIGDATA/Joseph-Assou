#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:37:39 2017

@author: joseph
"""

#labos , equivalents traitement, annee commer, mois commer, pris , rest age , rest poids, dosage

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

url=[]
labos=[]
equivalent =[]
traitement=[]
annee =[]
moiscommer=[]
poids =[]
restage=[]
restpoids =[]
dsage =[]
nom =[]
prix =[]

regexYear =r"\d+-\d+-(\d+)"
regexNumber = r"\(d+)"
regexAge = r"(\d+)\sans"
regexunit =r"\d+(.*)"
#pd.tonumeric


def getYearandMonth(data):
    
    if data != None:
        d =str(data).split("-")
        moiscommer.append(int(l[1]))
        annee.append(int(l[2]))
    else:
        moiscommer.append(0)
        annee.append(0)

    
def getNumber(data):
    
    number = re.search(regexNumber, str(data))
    if number != None:
        return number.group(0)
    else:
        return 0

def getAge(data):
    age = re.search(regexAge, data)
    if age != none:
        dsage.append(age.group(0))
    else:
        dsage.append('NA')


def getUnit(data):
    


def getJson():
       
    url = "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=ibuprofen"
    
    resapi = requests.get(url,)
    if resapi.status_code==200:
        data = js.loads(resapi.text)
    else:
        print('on vient de se faire jeter')
    
    print(data[0]['codeCIS'])

def geturl(data):
    url = []
    for d in data:
        url.append('https://www.open-medicaments.fr/api/v1/medicaments/'+d)



def getFeatures(url):
    
    resapi = requests.get(url,)   
    if resapi.status_code==200:
        data = js.loads(resapi.text)
    else:
        print('on vient de se faire jeter')
    
    if data['denomination'] != None:
        nom.append(data['denomination'])
    else:
        nom.append('NA') 
    if data['titulaires'][0] != None:
        labos.append(data['titulaires'][0])
    else:
        labos.append('NA')
    if data['presentations'][0]["prix"] !=None:
        prix.append(data['presentations'][0]["prix"])
    else:
        prix.append('NA')
        
    
    getYearandMonth(data['dateAMM'])
    refdosage = getNumber(data['compositions'][0]['referenceDosage'])
    subdosage = getNumber(data['compositions'][0]['substancesActives'][0]['dosageSubstance'])
    
    print(data["indicationsTherapeutiques"])
    
       

getFeatures('https://www.open-medicaments.fr/api/v1/medicaments/64565560')
