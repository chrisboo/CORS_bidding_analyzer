import bs4 as bs
import pandas as pd
import os.path
import urllib.request

def generateArchiveUrl(year, sem, rnd):
    return 'http://www.cors.nus.edu.sg/Archive/' + \
           str(year) + str("%02d" % (year % 100 + 1)) + \
           '_Sem' + str(sem) + '/successbid_' + rnd + '_' + \
           str(year) + str(year + 1) + 's' + str(sem) + '.html'

def generateFileName(year, sem, rnd):
    return 'successbid_' + str(year) + str(year + 1) + '_Sem' + str(sem) + '_' + rnd + '.csv'

print("Scrapping the contents...")

def scrape(year):
    while True:
        for sem in [1, 2]:
            rnds = [a + b for a in "123" for b in "AB"]
        
            if sem == 1:
                rnds.append("1C")

            rnds.sort()
            
            for rnd in rnds:
                url = generateArchiveUrl(year, sem, rnd)
                fname = generateFileName(year, sem, rnd)

                print("Reading " + url)
            
                if os.path.isfile(fname):
                    print("File already exist!")
                    continue

                try:
                    request = urllib.request.urlopen(url)
                    html = bs.BeautifulSoup(request.read(), 'lxml')

                    pageData = []
    
                    tableRows = html.find_all('tr')

                    for tr in tableRows:
                        td = tr.find_all('td')
                        row = [entry.text for entry in td]

                        # clean row
                        if len(row) < 9:
                            row = pageData[-1][0:2] + row[1:]

                        pageData.append(row)

                    df = pd.DataFrame.from_records(pageData[2:], columns=pageData[0])
                
                    df = df.apply(pd.to_numeric, errors='ignore')

                    df.to_csv(fname)
                    print("Created new file: " + fname)
                except Exception:
                    print("Webpage does not exist!")
                    print("Aborting...")
                    return True

        year += 1

scrape(2006)