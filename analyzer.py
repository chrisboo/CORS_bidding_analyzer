import math
import bs4 as bs
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt

main = 'http://www.cors.nus.edu.sg/'

rawHTML = urllib.request.urlopen(main + 'archive.html').read()

HTML = bs.BeautifulSoup(rawHTML, 'lxml')

outboundLinks = HTML.find_all('a', href=True)

urls = [link.get('href') for link in outboundLinks if link.get('href').startswith('./Archive') and "successbid" in link.get('href')]

def year(url):
    return int(url[10:16])

urls.sort(key=year)

years = list(set([year(url) for url in urls]))

years.sort()

print(years)

def query(module, faculty, sem, accType, newStudent):
    maxPoints = [0 for _ in range(len(years))]
    minPoints = [100000 for _ in range(len(years))]

    for url in urls:
        if "Sem" + str(sem) not in url:
            continue

        print(url)

        rawHTML = urllib.request.urlopen(main + url).read()
        HTML = bs.BeautifulSoup(rawHTML, 'lxml')

        pageData = []

        tableRows = HTML.find_all('tr')

        for tr in tableRows:
            td = tr.find_all('td')
            row = [entry.text for entry in td]

            # clean row
            if len(row) < 9:
                row = pageData[-1][0:2] + row[1:]

            pageData.append(row)

        # create pandas data frame
        df = pd.DataFrame.from_records(pageData[2:], columns=pageData[0])

        # remove unwanted columns
        df = df.drop(['Quota', 'NoofBidders', 'LowestBid', 'HighestBid'], axis=1)

        # change data type of all entries to numbers whenever possible
        df = df.apply(pd.to_numeric, errors='ignore')

        # filter new student
        if newStudent:
            df = df.drop(df[df['Student Type[Acct Type]'].str.contains("New Students")].index)

        # extract rows with the module code
        df = df[df['Module'] == module]

        # extract rows that is associated with your faculty
        if '_3' not in url:
            df = df[df['Faculty'] == faculty]

        maxPoint = df['LowestSuccBid'].max()
        minPoint = df['LowestSuccBid'].min()

        print(maxPoint, minPoint)

        if not math.isnan(maxPoint):
            maxIdx = years.index(year(url))
            maxPoints[maxIdx] = max(maxPoints[maxIdx], maxPoint)

        if not math.isnan(minPoint):
            minIdx = years.index(year(url))
            minPoints[minIdx] = min(minPoints[minIdx], minPoint)

    print(years)
    print(maxPoints)
    print(minPoints)

    plt.xticks(years, years)
    plt.plot(years, maxPoints)
    plt.plot(years, minPoints)
    plt.legend(['max', 'min'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()

query('MA1101R', 'SCHOOL OF COMPUTING', 1, 'PROGRAMME', False)