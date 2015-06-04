import requests
import os
import datetime
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth

def visit_links(list_of_links):
    bad_links = []

    for link in list_of_links:
        print link
        try:
            response = requests.get(link['url'])
            print response.status_code

            if(response.status_code == 404):
                bad_links.append(link)

        except requests.exceptions.RequestException as e:
            # catastrophic error. fail.
            print "It's likely that this domain doesn't exists anymore."
            print e
    write_to_file(bad_links)

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
