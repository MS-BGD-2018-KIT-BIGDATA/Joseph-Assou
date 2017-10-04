# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import time
import math
import random as rand
import numpy as np
from sklearn import linear_model
from os import mkdir

def QuoteOfTheday() :
    d = dict()
    d[0] = "We are Happy Data Scientist"
    d[1] = "Charles is real business Geek"
    return print (d[np.random.randint(0,2)])
QuoteOfTheday()
