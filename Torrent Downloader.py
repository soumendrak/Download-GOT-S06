import urllib2
from bs4 import BeautifulSoup
import requests
import subprocess
import time
from sms import texting
from email_code import sendemail
path = "C:\Users\Soumendra\AppData\Roaming\uTorrent\uTorrent.exe" #uTorrent path
def get_page(url):
    hdr={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    try:
        req = urllib2.Request(url, headers=hdr)     
        return urllib2.urlopen(req).read()
    except urllib2.URLError:
        return "No"      

def get_final_page(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")
    title = str(soup.title).replace("<title>","").replace("</title>","").replace("Download","")
    for link in soup.find_all('a'):
        if str(link.get('href'))[0:7] == 'magnet:':
            return str(link.get('href')), ">>"+title+"<<"

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
    #Returns the first URL of the page 
    #i.e. the link with maximum seeders

def go_to_torrent_page(page):
    kickFind='<a href="https://kat.cr'
    start_link=page.find(kickFind)
    if start_link==-1:
        kickFind='<a href="http://extratorrent.cc'
        start_link=page.find(kickFind)
        if start_link==-1:
            kickFind='<a href="https://thepiratebay.se'
            start_link=page.find(kickFind)
            if start_link==-1:
                return False
        
    page[start_link-3:]
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url
        
def main(Flag):
    searchItem=raw_input("Enter the torrent you wish to search:")
#     searchItem="Game of thrones S06E09"
    completeUrl="http://torrentz.com/search?q="+searchItem.replace(" ","+")
    pageContent=get_page(completeUrl)    
    newUrl="http://torrentz.com"+ str(go_to_next_page(pageContent))
    nextPageContent=get_page(newUrl)
    if nextPageContent == "No":
        print time.strftime('%X'), ":  File NOT avaiable yet"                
        return "N"
    finalUrl=go_to_torrent_page(nextPageContent)    
    if finalUrl==False:
        print "Can not process Ahead as URL not found"
        print "Go to this link: %s to download manually" %(finalUrl)
    else:        
        magnet, title=get_final_page(finalUrl)        
        if magnet==False:
            print "Error in finding the magnet link of the torrent"
            print "Go to this link: %s to download manually" %(finalUrl)
        else:
            print "The %s torrent is ready to download" %title
            Flag = 'Y'
            subprocess.Popen([path,magnet])
    return Flag, title

if __name__ == "__main__":
    Flag = 'N'
    while True:
        if Flag == 'N':
            Flag, title = main(Flag)
            if Flag != 'Y':
                time.sleep(1)                
        else:
            print time.strftime('%X'),":  Torrent downloaded"
            email = 'xxxxxxxxy3@gmail.com xxxxxxxxxilu@yahoo.com '
            number = '+91XXXXXXXXX +91XXXXXXXXX'
            message = 'Subject: Torrent status. \nThe file ' + title + ' is available now. Downloading it'
            texting(message, number)
            sendemail(email, message)
            break
