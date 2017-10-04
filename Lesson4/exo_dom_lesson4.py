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


def TopContributorsByCrawling():
    url = "https://gist.github.com/paulmillr/2657075"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    listContributors = soup.find_all("tr")
    contributorname = []
    contributorrating = []
    contributororigin = []

    
    for i in range(1,257):
        contributorname.append(listContributors[i].find_all("td")[0].find("a").text)
        contributorrating.append(int(listContributors[i].find_all("td")[1].text))
        contributororigin.append(listContributors[i].find_all("td")[2].text)
        
    
    
    df = pd.DataFrame({'Name': contributorname,'Rating': contributorrating,'Origin': contributororigin})
    print(df)

def main():
    
    TopContributorsByCrawling()

main()