import bs4 as bs
import urllib.request

def getSource(url):
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    urls = soup.find_all('a', href=True)

    return [url.get('href') for url in urls if url.get('href').startswith('./Archive') and "successbid" in url.get('href')]