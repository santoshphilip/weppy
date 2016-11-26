"""make the documentation url links"""

import requests
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup


def getmainurl(version=None):
    """get the mainurl"""
    if not version:
        mainurl = "http://bigladdersoftware.com/epx/docs/8-3/input-output-reference/"
        return mainurl

def getdocsoup(mainurl=None):
    """get the documentation txt in beautifulsoup"""
    if not mainurl:
        mainurl = getmainurl()
    try:
        r = requests.get(mainurl)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup
    except ConnectionError as e:
        html_doc = ""
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

def getdoclinks(soup):
    """return all links in the main doc page"""
    links = soup.find_all('a')
    linkdct = {link.text.upper():'%s%s' % (getmainurl(), link.get('href'))
                    for link in links}
    return linkdct
    
def getdoclink(key):
    """get the doclink"""
    try:
        link = doclinks[key]   
        return link
    except KeyError as e:
        return None

doclinks = getdoclinks(getdocsoup())
# doclinks = dict()
