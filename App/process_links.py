import requests
import os
import output
from link               import Link
from datetime           import datetime
from time               import gmtime, strftime
from urllib.parse       import urlparse, urljoin
from bs4                import BeautifulSoup

broken_links = []
links_to_crawl = []
crawled_urls = []
links_to_other_domains = []
root_domain = 'http://localhost:8000'
start_link = Link(root_domain, 'Start', 'root')

# Helper function to check if a url is of the same domain as given root domain
def url_is_of_same_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return True if domain == root_domain else False

# Visits a link with requests. If status code is 404
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
        print("It's likely that this domain doesn't exists anymore.")
        print(e)

def create_file_name():
    return datetime.now().strftime("%Y%m%d_%H-%M-%S") + '.html'

def write_to_file(file_content):
    print('now printing to file')
    # Getting the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, '..', 'output')

    # Try to open the destination directory, otherwise create it
    try:
        os.stat(dest_dir)
    except:
        os.mkdir(dest_dir)

    # Create file name with date and time of now
    file_name = create_file_name()
    file_object = open(os.path.join(dest_dir, file_name), "wt", encoding="UTF-8")
    file_object.write(file_content)
    file_object.close()

def make_absolute_of_relative(origin, url):
    # todo, this should be done with urlparser instead
    # If the urls are relative, they should be made absolute, using the given domain

    parsed = urlparse(url)
    if not is_absolute(url):
        parsed = urlparse(urljoin(root_domain, parsed.path))
    return url

# Given a string of a HTML and a link obejct from where the HTML was fetched, it returns all
# the links on that page.
def find_all_links(html, origin):
    soup = BeautifulSoup(html, "html.parser")
    # Get all a tags on the given html page
    a_tags = soup.find_all('a')
    linkObjects = []
    for a_tag in a_tags:
        # Get the urls and content of the a tags and save them as object in a list
        url = a_tag.get('href', '')
        title = ''.join(a_tag.get_text(" | ", strip=True))
        link = Link(url, title, origin)
        linkObjects.append(link)
    return linkObjects

def crawl(link):
    # this should also check for content type
    url = link.url
    r = requests.get(url)

    # Using encoding here, if not, all special characters got screwed up in the end
    r.encoding = 'utf-8'

    parsed_links = find_all_links(r.text, url)
    print('Found these links:')
    print(parsed_links)
    links_to_crawl.extend(parsed_links)

def check(link):
    url = link.url
    print('now checking ' + link.url)

    # Check if the link has alreade been checked
    if url in crawled_urls and url in [u.url for u in broken_links]:
        broken_links.append(link)
        print('already crawled it, and it was broken')
        return
    elif url in crawled_urls:
        print('already crawled it')
        return

    try:
        crawled_urls.append(url)
        r = requests.head(url)

        content_type = r.headers.get('content-type', '')
        print('content-type: ' + content_type)
        if not r.ok:
            print('not OK link')
            link.error = str(r.status_code)
            broken_links.append(link)
        else:
            print('OK link')
            if root_domain in url and 'text/html' in content_type:
                print('in same domain, and text/html')
                print('Should now crawl this page for new links')
                # todo, now it can check wrong here, if an external domain contains the root domain somehow
                crawl(link)

    except requests.exceptions.ConnectionError as e:
        broken_links.append(link)

def validate_url(url, origin):
    print('Validating url', url)
    parsed = urlparse(url)

    if parsed.hostname == None:
        print('no hostname')
        print('Link is relative')
        if parsed.scheme == 'mailto' or parsed.scheme == 'tel':
            print('Link is a mailto')
            should_be_crawled = False
        else:
            # parsed.scheme == 'http' or parsed.scheme == 'https':
            print('Link is not mailto')
            print('origin: ' + origin)
            should_be_crawled = True
            parsed = urlparse(urljoin(origin, parsed.path))
        # else:
        #     print 'Link is of unknown scheme'
        #     should_be_crawled = False
    else:
        should_be_crawled = True

    # By this time the url should be normalized, so all remaining ../ is not part of the path, byt will all resolve
    # to root. So are removing them here to not make infinite loops, and the urls in crawled_urls correct
    new_url = parsed.geturl().replace('/../', '/')

    print('New url is', new_url)
    # The following remove lilnks such as mailto
    return new_url, should_be_crawled

def start ():
    # Starting point, at least so far
    while links_to_crawl:
        link = links_to_crawl.pop()
        print('Now popping off a new link: ', link.url)

        url = link.url
        parsed_url, should_be_crawled = validate_url(url, link.origin)
        print('Should link be crawled? ', should_be_crawled)
        link.url = parsed_url

        if(should_be_crawled):
            check(link)

try:
    links_to_crawl.append(start_link)
    start()
    print('out of start')
    content = output.create_output_html(broken_links, root_domain)
    write_to_file(content)
except AttributeError as e:
    print('exception')
    print(e)
    print(broken_links)
    #write_to_file(broken_links)
except KeyboardInterrupt as e:
    print('Script was stoped by keyboard, printing what is gathered up until now')
    content = output.create_output_html(broken_links, root_domain)
    write_to_file(content)
