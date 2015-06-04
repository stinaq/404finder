from bs4 import BeautifulSoup

def findAllLinks(html):
    soup = BeautifulSoup(html)
    atags = soup.find_all('a')
    linkObjects = []
    for atag in atags:
        temp = {}
        temp['url'] = atag['href']
        temp['title'] = ''.join(atag.get_text("|", strip=True))
        linkObjects.append(temp)
    return linkObjects

html = open(".\index2.html")
allLinks = findAllLinks(html)
print allLinks
