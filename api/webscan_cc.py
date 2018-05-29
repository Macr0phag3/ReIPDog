# encoding: utf8
import requests
from re import *
import time
from ToolBox.putColor import *
from ToolBox.errordog import *
from termcolor import colored


def getIP(url):
    repeat = 10
    while repeat:
        try:
            html = eval(requests.get(
                'http://www.webscan.cc/?action=getip&domain='+url).text[1:])
            break
        except:
            time.sleep(1)
        repeat -= 1

    if repeat == 0:
        return 'Error', putColor('The api of webscan.cc is broken\n', 'red')

    IP = html['ip']
    Address = html['info'].decode('unicode-escape').encode('utf-8')
    return IP, Address


@ErrorDog('www.webscan.cc')
def search(Host, s):
    Sites = []
    print '[*]Using API of:', putColor('www.webscan.cc', 'magenta')
    api = 'http://www.webscan.cc/?action=query&ip='

    print '[+]Info'
    Host, Address = getIP(Host)
    print '  [-]', Host
    print '  [-]', Address
    if 'Error' in Host or 'Error' in Address:
        return []

    while 1:
        html = requests.get(api+Host).text
        if 'setTimeout' not in html:
            break
        time.sleep(1)

    html = findall('"domain":"(.+)","title":"(.*)"', html.replace(']', '\n').replace('}', '\n'))
    if not html:
        print '[+]Sites(0)\n'
        return []

    info = [
        [
            info[0].replace('\/', '/'),
            info[1].decode('unicode-escape').encode('utf-8')
        ]
        for info in html
    ]

    print '[+]Sites(%d)' % len(info)

    for i in info:
        if s:
            print '  [-]', i[0], ':', i[1]
        Sites.append(i[0])
    print
    return Sites
