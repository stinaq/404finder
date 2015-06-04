import requests
import get_links
import processLinks

def start (url):
    # Starting point, at least so far
    domain = 'http://stinaq.se'
    r = requests.get(url)
    full_html = r.text
    all_links = get_links.find_all_links(full_html, domain)

    processLinks.visitLinks(all_links)

start('http://stinaq.se/2015/06/en-sidan-med-massa-trasiga-lankar/')
