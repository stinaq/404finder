from bs4 import BeautifulSoup

def make_absolute_of_relative(url, domain):
    # If the urls are relative, they should be made absolute, using the given domain
    if url.startswith('/'):
        return domain + url
    return url

def find_all_links(html, domain):
    soup = BeautifulSoup(html)
    # Get all a tags on the given html page
    a_tags = soup.find_all('a')
    linkObjects = []
    for a_tag in a_tags:
        # Get the urls and content of the a tags and save them as object in a list
        url = a_tag['href']
        title = ''.join(a_tag.get_text("|", strip=True)).encode('utf-8')

        absolute_url = make_absolute_of_relative(url, domain)

        temp = {}
        temp['url'] = absolute_url
        temp['title'] = title

        linkObjects.append(temp)
    return linkObjects
