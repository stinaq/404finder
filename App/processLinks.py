import requests
import os
import datetime
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth

#headers = {'accept': 'application/json;odata=verbose'}
#r = requests.get('http://dev/', auth=HTTPBasicAuth('booldevlocal\\administrator', 'Booldev1'))

#print r

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
    write_to_file(bad_links, get_file_path())


def get_file_path():
    # Dafult path to user desktop
    file_path = os.path.expanduser('~\Desktop')
    # filePath  = raw_input("Enter desired file destination: ")
    return file_path


def write_to_file(link_objects, file_directory):

    # time to make file anme unique
    current_datetime = strftime("%Y%m%d_%H-%M-%S", gmtime())

    # adding a as second parameter to open means append to the end of file.
    file_object = open(file_directory + '\\brokenLinks' + current_datetime + '.txt', 'a')

    for link in link_objects:

        #substring title 30 characters
        title = link['title'][:29]

        #format output in columns
        file_object.write('{0:30}   {1:30}'.format(title, link['url']) + ' \n')
    file_object.close()


listOfLinks = [{'url':'http://google.com/lxfjdklj', 'title':'Google'},{'url':'http://google.com/dfdfgdfgfff', 'title':'Stina Qvartstrom is a girl on my job'}, {'url':'http://google.com/ogfjgiofjgi', 'title':'Malins Test'}, {'url':'http://jioijoj.com', 'title':'joijoj'}, {'url':'http://www.oppetarkiv.se//nostalgi', 'title':'Svt'}]

#path = enterFilePath()
#print path
#WriteToFile("Teeest!", "http://url.se", path)
#visit_links(listOfLinks)
