import requests
import os
import datetime
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth

#headers = {'accept': 'application/json;odata=verbose'}
#r = requests.get('http://dev/', auth=HTTPBasicAuth('booldevlocal\\administrator', 'Booldev1'))

#print r.json()["d"]["Title"]
#print r

def visitLinks(listOfLinks):
    for link in listOfLinks:
        print link
        try:
            response = requests.get(link['url'])
            print response.status_code
            if(response.status_code == 404):
                writeToFile(link, enterFilePath())
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print e


def enterFilePath():
    filePath = os.path.expanduser('~\Desktop')
   # filePath  = raw_input("Enter desired file destination: ")
    return filePath


def writeToFile(linkObject, fileDirectory):
    # adding a as second parameter to open means append to the end of file.
    #fileObject = open('C:\Users\Administrator\Desktop\Output.txt','a')
    currentDatetime = strftime("%Y%m%d_%H-%M-%S", gmtime())
    fileObject = open(fileDirectory + '\\brokenLinks' + currentDatetime + '.txt', 'a')
    fileObject.write(linkObject['title'] + '    ' + linkObject['url'] +' \n')
    fileObject.close()


listOfLinks = [{'url':'http://google.com/lxfjdklj', 'title':'Google'}, {'url':'http://jioijoj.com', 'title':'joijoj'}, {'url':'http://svt.se', 'title':'Svt'}]

#path = enterFilePath()
#print path
#WriteToFile("Teeest!", "http://url.se", path)
visitLinks(listOfLinks)
