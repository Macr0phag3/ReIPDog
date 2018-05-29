# encoding: utf8
import requests
from re import *
import time
from ToolBox.putColor import *
from ToolBox.errordog import *


def getInfo(html):
    Info = []
    for r in ['<strong class="red">(.+)</strong>', '<strong>(.+)</strong>', '<span class="red">(.+)</span>']:
        _ = findall(r, html)
        if _:
            Info.append(_[0])
        else:
            Info.append('null')

    if Info[-1].isdigit() == False:
        Info[-1] = '0'
    return ['  [-] '+'\n  [-] '.join(Info[:-1]), int(Info[-1])]


def getSites(html):
    hosts = findall('rel="nofollow" target="_blank">(.+)</a>', html)
    loading = findall('<td class="title">\s+(.+\s+</td>)', html)
    titles = []
    for l in loading:
        if 'loading' in l:
            titles.append('Loading')
        else:
            titles.append(''.join(findall('<span>(.*)</span>\s+</td>', l)[0].split('\t')))

    return hosts, (': '.join(i) for i in zip(hosts, titles))


def getLastPages(html):
    lpage = findall('([0-9]+)/"><i class="ico-pager-end"></i></a>', html)
    if lpage:
        return int(lpage[0])
    return 0


@ErrorDog('dns.aizhan.com')
def search(Host, s):
    api = 'https://dns.aizhan.com/'
    print '[*]Using API of:', putColor('dns.aizhan.com', 'magenta')
    html = requests.get(api+Host+'/').text

    page = getLastPages(html)

    print '[+]Info'
    Info = getInfo(html)
    print Info[0]
    print '[+]Sites(%d)' % Info[1]
    Sites = []
    # 多个页面
    if Info[1]:
        sites, Hosts = getSites(html)
        Sites.extend(sites)
        if s:
            print '  [-] ' + '\n  [-] '.join(Hosts)
        for i in range(2, page):
            time.sleep(1)
            html = requests.get(api+Host+'/%d/' % i).text
            sites, Hosts = getSites(html)
            Sites.extend(sites)
            if s:
                print '  [-]' + '\n  [-]'.join(Hosts)

    print
    return Sites
