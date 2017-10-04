#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:12:07 2017

@author: joseph
"""

## Web Scrapping
import requests
from bs4 import BeautifulSoup


def  MyfirstWebScrapp(): ##Scrpping Youtube
    url ='http://www.purepeople.com/article/laeticia-et-johnny-hallyday-leur-fille-jade-franchit-un-cap-avec-le-sourire_a252004/1'    
    res = requests.get(url)
    shareclass = 'c-sharebox__stats-number count'
    soup = BeautifulSoup(res.text, 'html.parser')
    print(int(soup.find_all(class_=shareclass).text.strip()))
    return res

def getSoupFromUrl(url, data='', method = 'get'):
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url,data=data )
    else:
        return none
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')    
        return soup
    else:
        return none
    
def getNuberOfSharedPeople(url, classname):
    soup = getSoupFromUrl(url)
    if soup :
        share_content = soup.find_all(class_=classname).text.strip()
        if K in share_content:
            parts = share_content[:-1].split(',')
            return int(parts[0]*1000 + int(parts[1]*1000))
        else:
            return int(share_content)
    else:
        return none

def getListOfAticle(people):
    url_search= 'http://www.purepeople.com/rechercher/'
    class_result = "c-article-flux_tite"
    url_search = "http://www.purepeople.com/rechercher/q/"+people+"/cat/article/np"
    result_search=[]
    soup_result_search=[]
    for i in range(1,4):
        soup_result_search += getSoupFromUrl(url_search+str(i))        
        result_search+=[a['href'] for a in soup_result_search.find_all("a", class_=class_result)]
    return result_search

all_page_people_1 = getListOfAticle('johnny')
all_page_people_1 = getListOfAticle('Angelina')

shares_people_1=[]
shares_people_2=[]

for page in all_pages_people_2:
    print ('--------')
    print (page)
    share = getNumberOfSharesForPage("http://www.purepeople.com" + page, share_calss_pp)
    print (share)
    shares_people_2.append(share)