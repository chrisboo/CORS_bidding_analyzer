import bs4 as bs
import urllib.request

def usefulSource(url):
    return url.startswith('./Archive') and "successbid" in url.get('href');

def getSource(url):
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    urls = soup.find_all('a', href=True)

    return [url.get('href') for url in urls if usefulSource(url.get('href'))]