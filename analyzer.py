import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def semester(fname):
    return int(fname[23])

def year(fname):
    return fname[11:19]

def biddingRound(fname):
    return fname[25:27]

def query(module, faculty, sem, accType, newStudent):
    location = './dataset/'

    maxResult = {}
    minResult = {}

    for fname in os.listdir(location):
        if fname == 'scraper.py' or semester(fname) != sem:
            continue

        df = pd.read_csv(location + fname)

        df = df.apply(pd.to_numeric, errors='ignore')

        # filter module and faculty
        df = df[df['Module'] == module]

        # filter faculty
        if biddingRound(fname)[0] != '3':
            df = df[df['Faculty'] == faculty]

        # filter newStudent
        if newStudent:
            df = df[(df['Student Type[Acct Type]'].str.contains("New Students")) | \
                    (df['Student Type[Acct Type]'].str.contains("NUS Students"))]
        else:
            df = df[(df['Student Type[Acct Type]'].str.contains("Returning Students")) | \
                    (df['Student Type[Acct Type]'].str.contains("NUS Students"))]
        
        # filter accType
        if accType == 'PROGRAMME':
            df = df[df['Student Type[Acct Type]'].str.contains('P')]
        else:
            df = df[df['Student Type[Acct Type]'].str.contains('G')]
        
        if df['LowestSuccBid'].count() == 0:
            continue

        maxRes = df['LowestSuccBid'].max()
        minRes = df['LowestSuccBid'].min()

        if maxResult.get(year(fname)) == None or maxResult[year(fname)] < maxRes:
            maxResult[year(fname)] = maxRes

        if minResult.get(year(fname)) == None or minResult[year(fname)] > minRes:
            minResult[year(fname)] = minRes

    maxResult = sorted(maxResult.items())
    minResult = sorted(minResult.items())

    maxX, maxY = zip(*maxResult)
    minX, minY = zip(*minResult)

    plt.plot(maxX, maxY)
    plt.plot(minX, minY)
    plt.show()

query('MA1101R', 'SCHOOL OF COMPUTING', 1, 'PROGRAMME', False)