import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def semester(fname):
    return int(fname[23])

def year(fname):
    return fname[11:19]

def biddingRound(fname):
    return fname[25:27]

def label(year):
    return 'AY' + year[2:4] + '/' + year[6:8]

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

    if len(maxResult) == 0:
        print("There is no result. Please check your query.")
        return False

    maxX, maxY = zip(*maxResult)
    minX, minY = zip(*minResult)

    # plot
    fig, ax = plt.subplots()
    topLine = ax.plot(maxY, 'ro-', label='Max lowestSuccBid among all rounds')
    botLine = ax.plot(minY, 'ko-', label='Min lowestSuccBid among all rounds')

    # label
    ax.set_xlabel('Academic Year', fontsize=12)
    ax.set_ylabel('Bid Points', fontsize=12)

    lines = topLine + botLine
    labels = [line.get_label() for line in lines]
    ax.legend(lines, labels, loc='upper center')

    # categorical xticks
    plt.xticks(range(len(maxX)), [label(year) for year in maxX], size='small')
    
    # force y-axis label to use only integers if maxY is too small
    if max(maxY) < 10:
        plt.yticks(range(math.ceil(max(maxY)) + 1))

    plt.suptitle('Bidding History for ' + module, fontsize=20)

    plt.show()

query('MA1101R', 'SCHOOL OF COMPUTING', 2, 'PROGRAMME', False)