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
regexTel = r"(\d(\s\-)?){10,11}"
mod=[]
loc=[]
km=[]
year=[]
price=[]
email=[]
modtyp=[]
cote=[]
Telephone=[]
telfromdesc=[]
prixneuf=[]
vendeurtype=[]
desclink=[]
description=[]
NextLink=[]

compteurBoncoin=0

def getPetitesAnnonces(marque, modele, region):
   
    url ="https://www.leboncoin.fr/voitures/offres/"+region+"/?th=1&q="+ modele+"&brd="+marque
    resAnnonce = requests.get(url)
    soup = BeautifulSoup(resAnnonce.text, 'html.parser')
    getLinkToNextPage(soup)
    soup =soup.find("section", class_="tabsContent block-white dontSwitch").find("ul")
    return soup

def getPetitesAnnoncesSuite(url):
   
    print(url)
    resAnnonce = requests.get(url)
    soup = BeautifulSoup(resAnnonce.text, 'html.parser')
#   getLinkToNextPage(soup)
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
    modeltype=['life', 'intens', 'zen']
    mod=[] 
    desclower = (str(des).lower())
    mod = re.search(regexModel, str(des),re.IGNORECASE)
    if mod != None:
        r=mod[1]
    else:
        r='NA'
    
    if r in modeltype:
        t=r
    elif modeltype [0] in desclower:
        t = modeltype[0]
    elif modeltype [1] in desclower:
        t = modeltype[1]
    elif modeltype [2] in desclower:
        t = modeltype[2]
    else:
        t = 'NA'
    modtyp.append(t)
    return t

def getTelFromDesc(desc):
    desclower = (str(desc).lower())
    tel = re.search(regexTel, desclower)
    if tel != None:
        telfromdesc.append(tel.group(0))
    else:
        telfromdesc.append('NA')
    


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
            'prix_neuf':prixneuf, 'TypeVendeur':vendeurtype,'telephone':Telephone,'email':email, 'lien' : desclink, 'telfromdesc': telfromdesc}
    DataZoe = pd.DataFrame(dico)
    DataZoe.to_csv('/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Lesson5/DataZoe.csv',  sep=';')
    
def getLinkToNextPage(soup):
    
    link = soup.find_all("a", class_="element page", href=True)
    link = list(map(lambda x: str('https:'+x['href']),link))
    print(link) 
    NextLink.append(link)
    print(NextLink)
    return(link)
    
    
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
    attente = np.random.randint(10,20)
    time.sleep(attente)    
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
    attente = np.random.randint(3,10)
    time.sleep(attente)
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
    attente = np.random.randint(5,15)
    time.sleep(attente)
    for url in desc:
        print(url)
        soupPA = getSoupAnnonce(url)
        listfeatures = getAnnonceFeatures(soupPA)
        getModel(listfeatures) 
        getTypeSeller(soupPA)
        d = getDesc(soupPA)
        getContactFromDesc(d)
        getTelFromDesc(d)
        getPhoneNumber(url)
        modelfeatures = [getModelfromDesc(d),
                         getYear(listfeatures), getKM(listfeatures), getloc(listfeatures)]
        getCote(modelfeatures,r)



def main():
    

    marque = "Renault"
    modele = "Zoe"
    region = ["ile_de_france", "provence_alpes_cote_d_azur","aquitaine"]
    desc=[]
    i=0
    for r in region:
        souplistpa = getPetitesAnnonces(marque,modele,r)        
        getPrice(souplistpa)
        desc=getPetitesAnnonceDescLink(souplistpa)
        getAllPageFeature(desc, r)
        fillDataframe()
        for link in NextLink[i]:
            souplistpa = getPetitesAnnoncesSuite(link)      
            getPrice(souplistpa)
            desc=getPetitesAnnonceDescLink(souplistpa)
            getAllPageFeature(desc,r)
            fillDataframe()
        i+=1
        

main()
