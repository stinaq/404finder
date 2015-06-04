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

