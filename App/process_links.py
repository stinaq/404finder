import requests
import os
import get_links
import datetime
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
from urlparse import urlparse

broken_links = []
links_to_crawl = []
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

def start (url):
    # Starting point, at least so far
    r = requests.get(url)
    full_html = r.text
    all_links = get_links.find_all_links(full_html, root_domain)

    visit_links(all_links)

start('http://stinaq.se/2015/06/en-sidan-med-massa-trasiga-lankar/')
