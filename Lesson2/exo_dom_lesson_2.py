#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 17:59:40 2017

@author: joseph
"""

import urllib
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd
import unittest




def getData(year):
    year.sort()
    a=np.arange((year[-1]-year[0]+1)*8).reshape(year[-1]-year[0]+1,8)
    i=0
    url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
    urllist=[]
    urllist= list(map(lambda y : url +str(y), year))
    for url in urllist:
        a[i]=GetElement2(url)
        i+=1
    nameCol=["A", "A1", "B", "B1","C", "C1", "D", "D1"]
    df=pd.DataFrame(a, index=year, columns=nameCol)
    return df    
    
#def GetElement(url):
#    montant=np.array([0,0,0,0])
#    res= requests.get(url)
#    soup = BeautifulSoup(res.text, 'html.parser')
#    mydivs=soup.find_all( class_ = "montantpetit G")
#    regex =r"(<td class=\"montantpetit G\">)(.*)\s</td>+"
#    montant[0] = int(re.search(regex,str(mydivs[2]))[2].replace(' ',''))
#    montant[1] = int(re.search(regex,str(mydivs[4]))[2].replace(' ',''))
#    montant[2] = int(re.search(regex,str(mydivs[10]))[2].replace(' ',''))
#    montant[3] = int(re.search(regex,str(mydivs[14]))[2].replace(' ',''))
##    print('for'+url +'we got the following: \n', montant)
#    return montant

def GetElement2(url):
    montant=np.array([0,0,0,0,0,0,0,0])
    regex =r"(<td class=\"montantpetit G\">)(.*)\s</td>+"
    res= requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    ResulTableA= soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")
    ResulTableB= soup.find("td", text="TOTAL DES CHARGES DE FONCTIONNEMENT = B").parent.find_all(class_ = "montantpetit G")
    ResulTableC= soup.find("td", text="TOTAL DES RESSOURCES D'INVESTISSEMENT = C").parent.find_all(class_ = "montantpetit G")
    ResulTableD= soup.find("td", text="TOTAL DES EMPLOIS D'INVESTISSEMENT = D").parent.find_all(class_ = "montantpetit G")
#    print(ResulTableB[2].text,ResulTableC[2].text,ResulTableD[2].text)
    for i in range(0,2):
        montant[i]=int(ResulTableA[i+1].text.replace(' ',''))
        montant[i+2]=int(ResulTableB[i+1].text.replace(' ',''))
        montant[i+4]=int(ResulTableC[i+1].text.replace(' ',''))
        montant[i+6]=int(ResulTableD[i+1].text.replace(' ',''))
    return montant
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES CHARGES DE FONCTIONNEMENT = B").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    montant[0] = int (soup.find("td", text="TOTAL DES PRODUITS DE FONCTIONNEMENT = A").parent.find_all(class_ = "montantpetit G")[1].text.replace(' ',''))
#    print(Inter)    

    
#Year=[2010,2011,2012,2013,2014,2015]
#print("Par defaut annes de 2010 à 2015 :\n" ,getData(Year))

    
def main()   :    
    
    Year=[2010,2011,2012,2013,2014,2015]
    print("Par defaut années de 2010 à 2015 :\n" ,getData(Year))

        
main()

#GetElement2("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013")
#test()
#test()

#class Lesson1Tests(unittest.TestCase):
#    
#    
#    a= np.array([[2449, 2449, 2241, 2241, 1119, 1119, 1265, 1265], [2546,2546,2327,2327, 1264,1264, 1268, 1268],
#        [2311, 2311, 2135, 2135, 1085, 1085, 1058, 1058], [2308, 2308, 2235, 2235, 1157, 1157, 1048, 1048],
#        [2365, 2365, 2294, 2294, 1066, 1066, 1048, 1048], [2322, 2322, 2354, 2354, 914, 914, 788, 788]])
#    nameCol=["A", "A1", "B", "B1","C", "C1", "D", "D1"]
#    Year=[2010,2011,2012,2013,2014,2015]
#    df=pd.DataFrame(a, index=Year, columns=nameCol)
#    #print(df)
#    
#    def testgetData(self):
#        Year=[2010,2011,2012,2013,2014,2015]
#        self.assertEqual(getData(Year), df)
#        
#    def clear_all():
#    #Clears all the variables from the workspace of the spyder application
#        gl = globals().copy()
#        for var in gl:
#            if var[0] == '_': continue
#            if 'func' in str(globals()[var]): continue
#            if 'module' in str(globals()[var]): continue
#        del globals()[var]
#
#
#
#    def main():
#        unittest.main()
#
#    if __name__ == '__main__':
#        clear_all()
#        main()
        
#GetElement("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2015")   