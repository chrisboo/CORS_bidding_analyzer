import bs4 as bs
import pandas as pd
import urllib.request

sauce = urllib.request.urlopen('http://www.nus.edu.sg/cors/Archive/201617_Sem1/successbid_1A_20162017s1.html').read()
soup = bs.BeautifulSoup(sauce, 'lxml')

table_rows = soup.find_all('tr')

data = []

for tr in table_rows:
 	td = tr.find_all('td')
 	row = [i.text for i in td]

 	if len(row) < 9:
 		row = [data[-1][0]] + [data[-1][1]] + row[1:]

 	data.append(row)

df = pd.DataFrame.from_records(data[2:], columns=data[0])

df = df.apply(pd.to_numeric, errors='ignore')

df = df.sort_values('LowestSuccBid', ascending=False)

print(df.head(10).ix[:, ['Module', 'LowestSuccBid']])