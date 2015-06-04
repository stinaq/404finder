from bs4 import BeautifulSoup

def make_absolute_of_relative(url, domain):
    if url.startswith('/'):
        return domain + url
    return url

def find_all_links(html, domain):
    soup = BeautifulSoup(html)
    a_tags = soup.find_all('a')
    linkObjects = []
    for a_tag in a_tags:
        url = a_tag['href']
        title = ''.join(a_tag.get_text("|", strip=True)).encode('utf-8')

        absolute_url = make_absolute_of_relative(url, domain)

        temp = {}
        temp['url'] = absolute_url
        temp['title'] = title

        linkObjects.append(temp)
    return linkObjects
