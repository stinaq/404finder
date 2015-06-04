from bs4 import BeautifulSoup

def make_absolute_of_relative(url, domain):
    if url.startswith('/'):
        return domain + url
    return url

