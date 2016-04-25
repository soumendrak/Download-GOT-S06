import urllib2
from bs4 import BeautifulSoup
import requests
import subprocess
import time
from sms import texting
from email_code import sendemail
from jdcal import gcal2jd
# uTorrent path change accordingly
path = "C:\Users\username\AppData\Roaming\uTorrent\uTorrent.exe"


def get_page(url):
    hdr = {'Accept': 'text/html,application/xhtml+xml,'
           'application/xml;q=0.9,*/*;q=0.8'}
    try:
        req = urllib2.Request(url, headers=hdr)
        return urllib2.urlopen(req).read()
    except urllib2.URLError:
        return "No"


def get_final_page(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "lxml")
    title = str(soup.title).replace("<title>", "").replace("</title>", "")
    title = title.replace("Download", "")
    for link in soup.find_all('a'):
        if str(link.get('href'))[0:7] == 'magnet:':
            return str(link.get('href')), ">>"+title+"<<"


def go_to_next_page(page):
    start_link = page.find('<div class="results"')
    page = page[start_link:]
    start_link = page.find("<dl>")
    end_link = page.find("</dl>")
    page = page[start_link:end_link]
    start_link = page.find("<a href=")
    if start_link == -1:
        return False
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1:end_quote]
    return url
    # Returns the first URL of the page
    # i.e. the link with maximum seeders


def go_to_torrent_page(page):
    kickFind = '<a href="https://kat.cr'
    start_link = page.find(kickFind)
    if start_link == -1:
        kickFind = '<a href="http://extratorrent.cc'
        start_link = page.find(kickFind)
        if start_link == -1:
            kickFind = '<a href="https://thepiratebay.se'
            start_link = page.find(kickFind)
            if start_link == -1:
                return False

    page[start_link-3:]
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1:end_quote]
    return url


def datecalc():
    dtime = [int(x) for x in time.strftime('%Y %m %d').split()]
    jd = int(gcal2jd(dtime[0], dtime[1], dtime[2])[1])
    std = 57503
    if (std >= jd) or jd > (std + 7):
        episode = "01"
    elif (std + 7 >= jd) or jd > std + 14:
        episode = "02"
    elif (std + 14 >= jd) or jd > std + 21:
        episode = "03"
    elif (std + 21 >= jd) or jd > std + 28:
        episode = "04"
    elif (std + 28 >= jd) or jd > std + 35:
        episode = "05"
    elif (std + 35 >= jd) or jd > std + 42:
        episode = "06"
    elif (std + 42 >= jd) or jd > std + 49:
        episode = "07"
    elif (std + 49 >= jd) or jd > std + 56:
        episode = "08"
    elif (std + 56 >= jd) or jd > std + 63:
        episode = "09"
    elif (std + 63 >= jd) or jd > std + 100:
        episode = "10"
    else:
        episode = "00"

    return episode


def main(Flag):
    # searchItem=raw_input("Enter the torrent you wish to search:")
    episode = datecalc()
    searchItem = "Game of thrones S06E"+episode
    completeUrl = "http://torrentz.com/search?q="+searchItem.replace(" ", "+")
    pageContent = get_page(completeUrl)
    newUrl = "http://torrentz.com" + str(go_to_next_page(pageContent))
    nextPageContent = get_page(newUrl)
    if nextPageContent == "No":
        print time.strftime('%X'), ":  File is NOT avaiable yet"
        return "N", ""
    finalUrl = go_to_torrent_page(nextPageContent)
    if finalUrl is False:
        print "Can not process Ahead as URL not found"
        print "Go to this link: %s to download manually" % (finalUrl)
    else:
        magnet, title = get_final_page(finalUrl)
        if magnet is False:
            print "Error in finding the magnet link of the torrent"
            print "Go to this link: %s to download manually" % (finalUrl)
        else:
            print "The %s torrent is ready to download" % title
            Flag = 'Y'
            subprocess.Popen([path, magnet])
    return Flag, title

if __name__ == "__main__":
    Flag = 'N'
    while True:
        if Flag == 'N':
            Flag, title = main(Flag)
            if Flag != 'Y':
                time.sleep(900)
        else:
            print time.strftime('%X'), ":  Torrent downloaded"
            email = "xxxxxx@yahoo.com xxxxxxxxxxx@gmail.com " \
                    "xxxxxxxxx@gmail.com xxxxxxxxxxx@outlook.com"
            print email
            number = '+91XXXXXXXXX +91XXXXXXXXXX'
            message = """ Subject: Torrent status.
            \nThe file """ + title + ' is available now. Downloading it '
            print message
            texting(message, number)
            sendemail(email, message)
            break
