import bs4 as bs
import urllib.request

def usefulSource(url):
    return url.startswith('./Archive') and "successbid" in url

def getSource(url):
    rawHTML = urllib.request.urlopen(url).read()
    HTML = bs.BeautifulSoup(rawHTML, 'lxml')

    outboundLinks = HTML.find_all('a', href=True)

    return [link.get('href') for link in outboundLinks if usefulSource(link.get('href'))]