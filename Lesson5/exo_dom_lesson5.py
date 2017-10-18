#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:04:24 2017

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





#année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
#Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

regexEmail = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\s*"
regexModel= r"Zoe\s(\w+)"
regexListId = r"(\d+).h"
regexPrice = r"(\d+)\s"
regexKM = r"(\d+)K"
regexCP =r"(\d+)"
mod=[]
loc=[]
km=[]
year=[]
price=[]
email=[]
modtyp=[]
cote=[]
Telephone=[]
prixneuf=[]
vendeurtype=[]
desclink=[]
description=[]

compteurBoncoin=0

def getPetitesAnnonces(marque, modele, region):
    
    url ="https://www.leboncoin.fr/voitures/offres/"+region+"/?th=1&q="+ modele+"&brd="+marque
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    soup =soup.find("section", class_="tabsContent block-white dontSwitch").find("ul")
    return soup

def getPetitesAnnoncesSuite(url):
    
    marque
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    soup =soup.find("section", class_="tabsContent block-white dontSwitch").find("ul")
    return soup


def getSoupAnnonce(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def getAnnonceFeatures(soup):
    listfeatures=[]
    listfeatures =soup.find_all("span", class_="value")
    return listfeatures
    
def getModel(listfeatures):
    Model = listfeatures[3].text
    mod.append(str(Model))
    #print(str(Model))
    return (str(Model))

def getloc(listfeatures):
    l = listfeatures[1].text
    loc.append(str(l))
    #print(str(l))
    return(str(l))    

def getKM(listfeatures):
    Km = listfeatures[5].text.replace(" ","")
    Km = re.search(regexKM,Km)
    km.append(int(Km[1]))
    #print(float(Km[1]))
    return int(Km[1])

def getYear(listfeatures):
    Year = listfeatures[4].text.replace(" ","")
    year.append(int(Year))
    return(int(Year))
    

def getPrice(soup):
#    price = re.search(regexPrice,strp)
    
    listpr =[]
    listpr = soup.find_all("h3", class_="item_price")
    strp= list(map(lambda x:x.text.replace(" ",""),listpr))
    price_item_page = list(map(lambda x: re.search(regexPrice,x)[1],strp))
    price.extend(price_item_page)
    print(price_item_page)
#    return(float(price))
    
def getPetitesAnnonceDescLink(soup):
    links = []
    links = soup.find_all("a", href=True)
    links = list(map(lambda x: str('https:'+x['href']),links))
    desclink.extend(links)
    return links

def getDesc(soup):
    description_ = []
    description_ = soup.find_all("p", class_="value")
    description_ = list(map(lambda x: str(x.text), description_))
    description.append(description_)
    return description_

def getContactFromDesc(desc):
    email_desc = re.search(regexEmail,str(desc))
    if email_desc != None:
        email.append(email_desc[1])
        print(email_desc[1])    
    else:
        email.append('NA') 
    

def getModelfromDesc(des):
    mod=[]
    print(des)
    mod = re.search(regexModel, str(des),re.IGNORECASE)
    print(mod)
    if mod != None:
        t=mod[1]
    else:
        t='NA'
    modtyp.append(t)
    return t

def getTypeSeller(soup):
    TypeSeller = soup.find_all("span", class_="ispro")
    if TypeSeller != []:
        vendeurtype.append(TypeSeller[0].text)
        print(TypeSeller[0].text) 
    else:
        vendeurtype.append('particulier')    
        print('particulier') 
    
def fillDataframe():
    dico =dict()
    dico = {'modele' :mod,'type':modtyp, 'année':year, 'kilometrage':km,'codepostal':loc, 'prix_vente':price, 'cote_affinée':cote,
            'prix_neuf':prixneuf, 'TypeVendeur':vendeurtype,'telephone':Telephone,'email':email}
    DataZoe = pd.DataFrame(dico)
    DataZoe.to_csv('/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Lesson5/DataZoe.csv',  sep='@@@@@')
    
def getLinkToNextPage(soup):
    soup1 = soup.find_all("div", class_="pagination_links_container")
    link = soup1[0].find_all('a', href=True)
    return(link[0]['href'])
    
    
def getPhoneNumber(url):
    global compteurBoncoin
    
    data=[]
    listeid = str(re.search(regexListId,url)[1])
    urlapi ='https://api.leboncoin.fr/api/utils/phonenumber.json'
    headers ={'Host': 'api.leboncoin.fr',
              'Connection': 'keep-alive',
              'Content-Length': '89',
              'Accept': '*/*',
              'Origin': 'https://www.leboncoin.fr',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Referer': url,
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4,it;q=0.2'}
    datainput = "list_id="+listeid+"&app_id=leboncoin_web_utils&key=54bb0281238b45a03f0ee695f73e704f&text=1"                                                      
    
    time.sleep(3)
    

    res = requests.post(urlapi, headers=headers, data=datainput)
    if (res.status_code ==200) :
        data = js.loads(res.text)
    else:
        print('on vient de se faire jeter')
        
        
    if 'phonenumber' in data['utils']:
        Tel = data['utils']['phonenumber']
        compteurBoncoin+=1
    else:
        Tel = "A prendre plus tard"    
    print(Tel)
    Telephone.append(Tel)
     
 
#def Select(model):
#     url='https://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html' 
#     res= requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
 
def getCote(modelfeatures,r):
    modeltype=['life', 'intens', 'zen']
    data=[]
    
    if r == 'ile_de_france':
        cp = str('75000')
    elif r == 'aquitaine':
        cp = str('33000')
    else:
        cp=str('13000')
        
    urlapi= "https://www.lacentrale.fr/get_co_prox.php?km="+str(modelfeatures[2])+"&zipcode="+str(cp)+"&month=01"
    
    if modelfeatures[0] in modeltype:
        url = "https://www.lacentrale.fr/cote-auto-renault-zoe-"+ str(modelfeatures[0]) + "+charge+rapide+type+2-"+ str(modelfeatures[1]) + ".html"
    else:
        url = "https://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide+type+2-"+str(modelfeatures[1])+".html"
   
    print(url)
    headers={
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4,it;q=0.2',
            'referer':url,
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
            }
    res = requests.get(url)
    cookie = res.cookies
    resapi = requests.get(urlapi,cookies=cookie, headers=headers)
    if resapi.status_code==200:
        data = js.loads(resapi.text)
    else:
        print('on vient de se faire jeter')
    print(data)
    cote_ = data['cote_perso']
    prix_neuf =data['price_new']
    print(cote_, prix_neuf)
    prixneuf.append(prix_neuf)
    cote.append(cote_)

def getAllPageFeature(desc,r):
    listfeatures=[]
    
    for url in desc:
        print(url)
        soupPA = getSoupAnnonce(url)
        listfeatures = getAnnonceFeatures(soupPA)
        getModel(listfeatures) 
        getTypeSeller(soupPA)
        d = getDesc(soupPA)
        getContactFromDesc(d)
        getPhoneNumber(url)
        modelfeatures = [getModelfromDesc(d),
                         getYear(listfeatures), getKM(listfeatures), getloc(listfeatures)]
        getCote(modelfeatures,r)
        
def main():
    
    marque = "Renault"
    modele = "Zoe"
    region = ["ile_de_france", "provence_alpes_cote_d_azur","aquitaine"]
    desc=[]
    
    for r in region:
        souplistpa = getPetitesAnnonces(marque,modele,r)        
        getPrice(souplistpa)
        desc=getPetitesAnnonceDescLink(souplistpa)
        getAllPageFeature(desc, r)
        lien = getLinkToNextPage
        print(lien)
        fillDataframe()
        while lien != None:
            souplistpa = getPetitesAnnoncesSuite(lien)      
            getPrice(souplistpa)
            desc=getPetitesAnnonceDescLink(souplistpa)
            getAllPageFeature(desc)
            lien = getLinkToNextPage    
            fillDataframe()
   

main()