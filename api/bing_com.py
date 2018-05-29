# -*- coding: utf-8 -*-
import re
import requests
import time
from ToolBox.putColor import *
from ToolBox.errordog import *
from xml.dom.minidom import parseString

Session = requests.session()


def getXMLData(xmlstring):
    ret = parseString(xmlstring)
    if len(ret.getElementsByTagName('title')) > 2:
        title = [node.childNodes[0].data for node in ret.getElementsByTagName('title')[2:]]
        url = [node.childNodes[0].data for node in ret.getElementsByTagName('link')[2:]]
        return title, url
    return [], []


def getXML(url, page=0):
    global Session
    Titles = []
    Urls = []
    if page:
        xmlstring = Session.get(url.replace('ensearch=0', 'ensearch=1') +
                                str(page)).text.encode('utf8')
        Titles, Urls = getXMLData(xmlstring)

    xmlstring = Session.get(url+str(page)).text.encode('utf8')
    title, url = getXMLData(xmlstring)
    Titles.extend(title)
    Urls.extend(url)
    return Titles, Urls


@ErrorDog('bing.com')
def search(Host, s):
    url = 'http://www4.bing.com/search?format=rss&ensearch=0&q=ip:%s&first=' % Host
    # url = 'https://cn.bing.com/search'

    print '[*]Using API of:', putColor('bing.com', 'magenta')

    # ----------- 反反爬 Bing ---------
    i = 11
    while i:
        _, data = getXML(url)
        if data:
            break
        i -= 1
    else:
        print '[!]Sites(0)\n'
        return []
    # ------------- end --------

    page = 1
    Sites = []
    Titles = []
    while 1:
        titles, sites = getXML(url, page)
        page += len(Sites)
        for site, title in zip(sites, titles):
            for rep in [r'\bhttps{0,1}://', r'\bwww\.', '/.*']:
                site = re.sub(rep, '', site)

            if site not in Sites:
                Sites.append(site)
                Titles.append(title)

        if not sites or len(sites) < 10:
            break

    print '[!]Sites(%d)' % len(Sites)
    if s:
        print '  [-]'+'\n  [-]'.join('%s: %s' % (i, j) for i, j in zip(Sites, Titles))

    print
    return Sites
