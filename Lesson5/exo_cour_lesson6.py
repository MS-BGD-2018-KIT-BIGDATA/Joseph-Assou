#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 13:42:22 2017

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
import walletstore as  wal


def importdata():
    dfmedecin= pd.read_csv('/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Lesson6/DAMIR/fichiers_supplementaires/rpps/rpps_tab3.csv',',')
 #   dfcat = pd.read_csv('/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Lesson6/DAMIR/fichiers_supplementaires/rpps/correspondance_rpps_damir_r.csv',';')
    dfcat1 = pd.read_csv('/home/joseph/Dropbox/DeepLearning/Programmation/Python/KitDataScience/Joseph-Assouline/Lesson6/DAMIR/fichiers_supplementaires/rpps/correspondance_rpps_damir_r_l_exe_spe.csv',',')
    
    print(dfmedecin.columns)
 #   print(dfcat.columns)
    print(dfcat1.columns) 
    return (dfmedecin)
            
importdata()




