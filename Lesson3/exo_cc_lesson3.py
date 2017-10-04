#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:31:41 2017

@author: joseph
"""
#lpTBk > div.lpTopTDG > div > ul > li:nth-child(1) > div > form > div.prdtBZPrice > div.prdtPrice

import urllib
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
import functools as ft

def getElementPrice(url, marque):
    i=0
    rebate=[]
    oldPrice=[]
    NewPrice=[]
    res= requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    regex =r"(<span class=\"price\">)(.*)<sup>+"
    regexold=r"(<div class=\"prdtPrSt\">)(.*)</div>+"
    Result = soup.find_all("div", class_="prdtBloc")
   
    for i in range(0,len(Result)):

        oldPricetext = Result[i].find("div", class_="prdtPrSt")
        if Result[i].find("span", class_="price") is not None:
            NewPricer = re.search(regex , str(Result[i].find("span", class_="price")))[2]
            NewPrice.append(float(NewPricer.replace(' ', '').replace(',','.')))
        else:
            break
            
        if oldPricetext != None:
            OldPricer = oldPricetext.text.replace(' ', '').replace(',','.')
            oldPrice.append(float(OldPricer))
        else:
            oldPrice.append(NewPrice[i]) 
        
        
        rebate.append((NewPrice[i]-oldPrice[i])/oldPrice[i])
        
    print(rebate)
    moy = ft.reduce(lambda x, y: x + y, rebate) / len(rebate)
    print("la moyenne de remise pour " + marque +" est : ", moy)

def main():
    url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html"
    url2="https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-lenovo.html"
    url3="https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-dell.html"
    getElementPrice(url, "acer")
    getElementPrice(url2, "lenovo")
    getElementPrice(url3, "dell")

main()

def testregexp():
    
    s = '<span class="price">429<sup>€100</sup></span>'
    regex =r"(<span class=\"price\">)(.*)<sup>+"
    res=re.search(regex,s)
    print(res[2])
    



#lpBloc
#<div class="prdtPrice"><span class="price">134<sup>€99</sup></span></div>
#<div class="prdtPrSt">139,99</div>
#<li data-sku="NXGPAEF002"><div class="prdtBloc">                   
#<span class="price">599<sup>€99</sup></span>