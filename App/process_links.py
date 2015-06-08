import requests
import os
import get_links
import datetime
from link import Link
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup

broken_links = []
links_to_crawl = []
crawled_urls = []
links_to_other_domains = []
root_domain = 'http://variadic.me/'

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
        response = requests.get(link.url)
        if(response.status_code == 404):
            broken_links.append(link)
        if(response.status_code == 200):
            if(url_is_of_same_domain(link.url)):
                links_to_crawl.append(link)
            else:
                links_to_other_domains.append(link)

    except requests.exceptions.RequestException as e:
        # catastrophic error. fail.
        print "It's likely that this domain doesn't exists anymore."
        print e

def write_to_file(link_objects):
    print 'now printing to file'
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
        error = link.error if hasattr(link, 'error') else ''
        #substring title 30 characters
        title = link.title[:29]

        #format output in columns
        file_object.write('{0:30}   {1:30}'.format(title, link.url) + error + ' \n')
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

        link = Link(absolute_url, title, origin)

        linkObjects.append(link)
    return linkObjects

def crawl(link):
    # this should also check for content type
    url = link.url
    r = requests.get(url)
    content_type = r.headers['content-type'] if hasattr(r.headers, 'content-type') else ''
    print 'content-TYPE' + content_type
    parsed_links = find_all_links(r.text, url)
    links_to_crawl.extend(parsed_links)

def check(link):
    url = link.url
    print 'now checking ' + link.url

    # Check if the link has alreade been checked
    if url in crawled_urls and url in [u.url for u in broken_links]:
        broken_links.append(link)
        print 'already crawled it, and it was broken'
        return
    elif url in crawled_urls:
        print 'already crawled it'
        return

    try:
        crawled_urls.append(url)
        r = requests.head(url)
        content_type = r.headers['content-type'] if hasattr(r.headers, 'content-type') else 'text/html'
        if not r.ok:
            print 'not OK link'
            link.error = str(r.status_code)
            broken_links.append(link)
        else:
            print 'OK link'
            if root_domain in url and 'text/html' in content_type:
                print 'in same domain, and text/html'
                # todo, now it can check wrong here, if an external domain contains the rott domain somehow
                crawl(link)

    except requests.exceptions.ConnectionError as e:
        broken_links.append(link)

def invalid_url(url):
    return True if url.startswith('#') or url == '' or url.startswith('mailto') else False

def validate_url(url, origin):
    parsed = urlparse(url)
    print '=============== url'
    print url
    if parsed.hostname == None:
        print '=============== hos no hostname'
        parsed = urlparse(urljoin(origin, parsed.path))
    print '=============== parsed'
    print parsed.geturl()
    return parsed.geturl()

def start ():
    # Starting point, at least so far
    while links_to_crawl:
        link = links_to_crawl.pop()

        url = link.url
        parsed_url = validate_url(url, link.origin)
        link.url = parsed_url

        if invalid_url(parsed_url):
            pass
        elif root_domain in link.url:
            print 'link on same domain'
            # print link
            crawl(link)
        else:
            print 'link on another domain'
            # print link
            check(link)

start_link = Link('http://variadic.me/', 'Start', 'root')
links_to_crawl.append(start_link)

try:
    start()
    print 'out of start'
    write_to_file(broken_links)
except AttributeError as e:
    print e
    print broken_links
