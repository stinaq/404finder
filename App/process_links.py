import requests
import os
import get_links
import datetime
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
from urlparse import urlparse
from bs4 import BeautifulSoup

broken_links = []
links_to_crawl = []
crawled_urls = []
links_to_other_domains = []
root_domain = 'http://stinaq.se/'

def url_is_of_same_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return True if domain == root_domain else False

def print_all_the_things():
    print '======================== broken_links ========================'
    for link in broken_links:
        print link

    print '======================== links_to_crawl ========================'
    for link in links_to_crawl:
        print link

    print '======================== links_to_other_domains ========================'
    for link in links_to_other_domains:
        print link

def visit_links(list_of_links):
    for link in list_of_links:
        visit_link(link)

    write_to_file(broken_links)
    print_all_the_things()

def visit_link(link):
    try:
        response = requests.get(link['url'])
        if(response.status_code == 404):
            broken_links.append(link)
        if(response.status_code == 200):
            if(url_is_of_same_domain(link['url'])):
                links_to_crawl.append(link)
            else:
                links_to_other_domains.append(link)
            
    except requests.exceptions.RequestException as e:
        # catastrophic error. fail.
        print "It's likely that this domain doesn't exists anymore."
        print e

def write_to_file(link_objects):
    # Getting the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, '..', 'output')

    # Try to open the destination directory, otherwise create it
    try:
        os.stat(dest_dir)
    except:
        os.mkdir(dest_dir)

    # Create file name with date and time of now
    file_name = strftime("%Y%m%d_%H-%M-%S", gmtime()) + '.txt'

    file_object = open(os.path.join(dest_dir, file_name), 'a')

    for link in link_objects:
        #substring title 30 characters
        title = link['title'][:29]

        #format output in columns
        file_object.write('{0:30}   {1:30}'.format(title, link['url']) + ' \n')
    file_object.close()

def make_absolute_of_relative(url, domain):
    # If the urls are relative, they should be made absolute, using the given domain
    if url.startswith('/'):
        return domain + url
    return url

def find_all_links(html, origin):
    soup = BeautifulSoup(html)
    # Get all a tags on the given html page
    a_tags = soup.find_all('a')
    linkObjects = []
    for a_tag in a_tags:
        # Get the urls and content of the a tags and save them as object in a list
        url = a_tag.get('href', '')
        title = ''.join(a_tag.get_text("|", strip=True)).encode('utf-8')

        absolute_url = make_absolute_of_relative(url, root_domain)

        temp = {}
        temp['url'] = absolute_url
        temp['title'] = title
        temp['origin'] = origin

        linkObjects.append(temp)
    return linkObjects

def crawl(link):
    url = link['url']
    if url in crawled_urls and url in [u['url'] for u in broken_links]:
        broken_links.append(link)
        return
    elif url in crawled_urls:
        return

    r = requests.get(url)
    if not r.ok:
        broken_links.append(link)
        return

    crawled_urls.append(url)
    links_to_crawl.extend(find_all_links(r.text, url))

def check(link):
    try:
        r = requests.head(link['url'])
        if not r.ok:
            broken_links.append(link)
    except requests.exceptions.ConnectionError as e:
        broken_links.append(link)

def start ():
    # Starting point, at least so far
    while links_to_crawl:
        link = links_to_crawl.pop()
        if link['url'].startswith('#'):
            pass
        elif root_domain in link['url']:
            print 'link on same domain'
            print link
            crawl(link)
        else:
            print 'link on another domain'
            print link
            check(link)

        # try:
        # crawl(links_to_crawl.pop())
        # except:
            # print broken_links


links_to_crawl.append({'url':'http://stinaq.se/2015/06/en-sidan-med-massa-trasiga-lankar/','title':'','origin':'root'})

try:
    start()
    write_to_file(br)
except AttributeError:
    print broken_links