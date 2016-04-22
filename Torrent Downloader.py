#-------------------------------------------------------------------------------
# Name:        Search new torrent and Download
# Purpose:
#
# Author:      Nagraj Gajengi
#
# Created:     12/21/2014
#-------------------------------------------------------------------------------
#change the client path
import urllib2
from bs4 import BeautifulSoup
import requests
import subprocess
import time
a = []
path = "C:\Users\Soumendra\AppData\Roaming\uTorrent\uTorrent.exe"
def get_page(url):
    hdr={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = urllib2.Request(url, headers=hdr)    
    return urllib2.urlopen(req).read()

def get_final_page(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    print str(soup.title)
    for link in soup.find_all('a'):
        a.append(link.get('href'))
        print str(link.get('href'))
    for i in range(len(a)):
        if a[i][0:7] == 'magnet:':
#             print a[i]
            return a[i], str(soup.title)
            break  

def go_to_next_page(page):
    start_link=page.find('<div class="results"')
    page=page[start_link:] 
    start_link=page.find("<dl>")
    end_link=page.find("</dl>")
    page=page[start_link:end_link]
    start_link=page.find("<a href=")
    if start_link==-1:
        return False
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url

def go_to_torrent_page(page):
    kickFind='<a href="https://kat.cr'
    start_link=page.find(kickFind)
    if start_link==-1:
        kickFind='<a href="http://extratorrent.cc'
        start_link=page.find(kickFind)
        if start_link==-1:
            kickFind='<a href="https://thepiratebay.se'
            return False
        
    page[start_link-3:]
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url
        
if __name__ == "__main__":
    searchItem=raw_input("Enter the torrent you wish to search:")
    completeUrl="http://torrentz.com/search?q="+searchItem.replace(" ","+")
    pageContent=get_page(completeUrl)    
    newUrl="http://torrentz.com"+ str(go_to_next_page(pageContent))
    print 'newUrl', newUrl
    nextPageContent=get_page(newUrl)
    finalUrl=go_to_torrent_page(nextPageContent)
    print "final URL", finalUrl
    if finalUrl==False:
        print "Can not process Ahead"
    else:        
        print "this is the final URL", finalUrl
        magnet, title=get_final_page(finalUrl)        
        if magnet==False:
            print "Error in finding torrent"
        else:
            print "Torrent downloading is "+title
#             p = subprocess.Popen([path,magnet])
