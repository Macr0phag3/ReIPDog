# -*- coding: utf-8 -*-
import requests
import sys
from putColor import *
from threadpool import *
import re

Sites = []
result = []


def getStatus(url):
    response = requests.get(url, timeout=5)
    title = re.findall('<title>(.+)</title>', response.text)
    site = url.replace('http://', '')
    if title:
        try:
            return putColor('  [√] ', 'green')+site+': '+putColor(title[0].encode('utf8'), 'cyan')
        except:
            return putColor('  [√] ', 'green')+site+': '+putColor('Encoding error', 'cyan')
    else:
        return putColor('  [!] ', 'yellow')+site+': '+putColor(str(response.status_code), 'cyan')


def Checking(site):
    global Sites, result
    # sys.flushout()
    try:
        result.append(getStatus('http://www.'+site))
        loc = Sites.index(site)
        Sites[loc] = Sites[loc].replace(site, 'www.'+site)
    except Exception, e:
        try:
            result.append(getStatus('http://'+site))
        except:
            result.append(putColor('  [X] ', 'red')+site)
            Sites.remove(site)


def Checker(name, s):
    global Sites
    with open('result/'+name+'.txt', 'r') as fp:
        Site = [site.replace('\n', '') for site in fp.readlines()]

    Sites = Site[:]
    n = min(len(Site), 20)
    pool = ThreadPool(n)
    queue = makeRequests(Checking, Site)
    [pool.putRequest(req) for req in queue]
    pool.wait()

    print '[!]Finished[%s]' % putColor(str(len(Sites)), 'cyan')
    print '\n'.join(result)
    pool.dismissWorkers(n, do_join=True)

    if len(Sites):
        with open('result/'+name+'_Alive.txt', 'w') as fp:
            fp.write('\n'.join(Sites)+'\n')
        print '\n[!]Saving Alive Sites to', putColor(name+'_Alive.txt', 'cyan')


# Checker('47_90_29_53')
