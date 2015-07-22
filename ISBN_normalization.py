__author__ = 'torresal'

"""# Notes #
- update entries in GCIS by using the GCIS API
- use the book identifier in GCIS API to update ISBN in GCIS
- Cause of 'Problem'
        - Does not have isbn
        - Does not have randomly generated identifier"""

import re, sys, requests
from isbnlib import EAN13, clean, to_isbn13

#Parses url.json#
def parse(url):
    import requests
    r = requests.get(url, verify = False)
    JSONdict = r.json()
    return JSONdict
GCIS = 'https://gcis-search-stage.jpl.net:3000/book.json?all=1'
GCISPAR = parse(GCIS)

for x in range(len(GCISPAR)):
    try:
#Extracts book identifier from GCIS#
        IDEN = GCISPAR[x]["identifier"]
        match =  re.search(r'.*/(.*?)\..*?$', GCIS)
        if match:
            FILETYPE = match.groups()[0]
#HREF = url that leads to book.json in GCIS-DEV
        HREF = 'https://gcis-search-stage.jpl.net:3000/{}/{}.json' .format(FILETYPE,IDEN)
        #HREF = 'https://gcis-search-stage.jpl.net:3000/book/13b8b4fc-3de1-4bd8-82aa-7d3a6aa54ad5.json'
        HREFPAR = parse(HREF)
#Extracts book title and isbn from GCIS-DEV
        d = dict(HREFPAR)
        TITLE = d['title']
        ISBNS = d['isbn']
#Cleans ISBNS to only conatian valid characters
        CISBN = clean(ISBNS)
#Converts all listed ISBNS to a ISBN-13 format
        C13 = to_isbn13(CISBN)
#V13 = validated canonical ISBN-13
        V13 = EAN13(C13)
        M = parse(HREF)
        MV13 = M["isbn"] = V13
        ORGISBN = M["org_isbn"] = ISBNS
        print(M, '\n\t', "isbn_original:", ISBNS)
        s = requests.Session()
        s.auth = ('alex' , '8aed39fa67049cdfd42ef612a97e8535ecd46d8955afcc8b')
        s.headers.update({'Accept': 'application/json'})
        r = s.post(HREF, data = M , verify = False)
        r.raise_for_status()
        sys.exit()
        #print('Title:', TITLE, '\nIdentifier:', IDEN,'\n',HREF,'\n\tISBN:', V13, '\n')
    except(TypeError, ValueError):
            print('\n\t######## PROBLEM #######\n','\tTitle:', TITLE,'\n\tGCIS-ISBN:', ISBNS,'\n\tIdentifier:', IDEN, '\n\n')













