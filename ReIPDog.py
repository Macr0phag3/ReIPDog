from urlparse import *
import re
from ToolBox.putColor import *
from ToolBox.AliveChecker import *
import sys
import argparse
import time
import datetime

import api.dns_aizhan_com as dns_aizhan_com
import api.webscan_cc as webscan_cc
import api.site_ip138_com as site_ip138_com
import api.bing_com as bing_com


def Saving(name, Sites):
    with open('result/%s.txt' % name, 'w') as fp:
        fp.write('\n'.join(Sites)+'\n')

        print '\n[!]Saving result to %s' % putColor(name+'.txt', 'blue')


def Analyse(Sites):
    for site in Sites:
        if site.count('.') == 1:
            print '[+]', putColor(site, 'green')
            Sites.remove(site)
            for s in Sites:
                if site in s:
                    print '  [-]', putColor(s, 'yellow')
                    Sites.remove(s)

    for site in Sites:
        print '[+]', putColor(site, 'green')


def Clean(Sites):
    Sites = list(set(Sites))
    for i, site in enumerate(Sites):
        site = re.sub(r'\bhttps{0,1}://', '', site)
        site = re.sub(r'\bwww\.', '', site)
        Sites[i] = site

    Sites = sorted(list(set(Sites)))
    return Sites[:]


print putColor('''
x------------------------------------------------------------x
.______     _______  __  .______  _______   ______   _______
|   _  \   |   ____||  | |   _  \|       \ /  __  \ /  _____|
|  |_)  |  |  |__   |  | |  |_)  |  .--.  |  |  |  |  |  __
|      /   |   __|  |  | |   ___/|  |  |  |  |  |  |  | |_ |
|  |\  \--.|  |____ |  | |  |    |  '--'  |  `--'  |  |__| |
| _| `.___||_______||__| | _|    |_______/ \______/ \______|

x------------------------------------------------------------x
''', 'cyan')
print '[*]Searching[%s]' % putColor(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'yellow')
starttime = datetime.datetime.now()
parser = argparse.ArgumentParser(usage='''

(sudo) (python) ReIPDog.py ip|host|url (1|0)

Such as:
Searching sites for ip -- 127.0.0.1 and output all info:
python ReIPDog.py -host 127.0.0.1

Searching sites for url -- google.com and do not show info:
python ReIPDog.py -host google.com --noutput

Version: 1.0; Running in Py2.x
''')

parser.add_argument("-host", default='HostsList', help="ip/url/host host you want to search")
parser.add_argument("--noutput", dest='s', action='store_false', help="output all info")
parser.add_argument("--set", dest='z', action='store_false', help="Merge the results")
args = parser.parse_args()

s = int(args.s)
HostsList = args.host
z = args.z

if HostsList == 'HostsList':
    try:
        with open('HostsList', 'r') as fp:
            HostsList = [''.join(i.split()) for i in fp.readlines() if len(i) > 4]
            if not HostsList:
                sys.exit(putColor('[X]', 'red')+'HostsList is empty')
    except Exception, e:
        if str(e):
            sys.exit(putColor('[X]', 'red')+'Where is your HostsList?')
else:
    HostsList = [HostsList]

Sites = []
for Host in HostsList:
    Host = urlparse(Host)
    Host = Host.netloc if Host.netloc else Host.path
    print '[!]Searching Sites for:', Host, '\n'
    if Host == '':
        print putColor('[X]', 'red')+'Error Host or IP'
        continue

    # ---------------- API ----------------------

    Sites.extend(dns_aizhan_com.search(Host, s))
    Sites.extend(webscan_cc.search(Host, s))
    Sites.extend(site_ip138_com.search(Host, s))
    Sites.extend(bing_com.search(Host, s))

    # ---------------- end ----------------------

    Sites = Clean(Sites)

    name = 0
    if len(Sites) and z:
        name = Host.replace('.', '_')
        print '[*]All Sites(%s)' % putColor(str(len(Sites)), 'cyan')
        Sites.sort()
        if s:
            Analyse(Sites[:])
        Saving(name, Sites)
        Sites = []
        print '\n[*]Check for Alive'
        Checker(name, s)

    print '-'*20, '\n'

if len(Sites) and not z:
    Sites.sort()
    print '[*]All Sites(%s)' % putColor(str(len(Sites)), 'cyan')
    if s:
        Analyse(Sites[:])
    name = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    Saving(name, Sites)


print '[!]Searching Finished'
if name and not z:
    print '-'*20
    print '\n[*]Check for Alive'
    Checker(name, s)

print '[!]All Done[%s]' % putColor(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'yellow')
endtime = datetime.datetime.now()
delta = (endtime - starttime).seconds
print '[*]Cost time:', putColor([''.join([i, j])
                                 for i, j in zip([str(delta), '%.2f' % (delta/60.0), '%.2f' % (delta/3600.0)],
                                                 [' s', ' m', ' h'])
                                 if i > '1'][-1], 'yellow')

print putColor('Having a nice day :)', 'green')
