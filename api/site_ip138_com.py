# encoding: utf8
import requests
from re import *
import time
from ToolBox.putColor import *
from ToolBox.errordog import *


@ErrorDog('site.ip138.com')
def search(Host, s):
    print '[*]Using API of:', putColor('site.ip138.com', 'magenta')
    Session = requests.session()

    # get the First Page
    html = Session.get('http://site.ip138.com/'+Host+'/').text
    # print html
    Info = []
    Address = findall('<h3>(.+)</h3>', html)
    if Address:
        Info.append(Address[0])
    else:
        Info.append('null')
    Hosts = [Host]
    if 'curadress' in html:
        IP = Session.get('http://site.ip138.com/domain/read.do?domain=%s' % Host).json()

        if str(IP['status']).lower() != 'false' and 'data' in IP:
            for ip in IP['data']:
                Info.append(ip['ip'])
        Info[0] += '(%d)' % (len(Info)-1)

        Hosts = Info[1:]

    print '[+]Info'
    print '  [-]', '\n  [-] '.join(Info)
    Sites = []
    for Host in Hosts:
        html = Session.get('http://site.ip138.com/'+Host+'/').text
        sites = findall('<li><span class="date">.+" target="_blank">(.+)</a></li>', html)
        for site in sites:
            if site not in Sites:
                Sites.append(site)

        _TOKEN = findall("var _TOKEN = '(.+)';", html)
        if _TOKEN:
            # get All Page from 2 to end.
            i = 2
            while 1:
                sites = Session.get('http://site.ip138.com/index/querybyip/?ip=%s&page=%d&token=%s' %
                                    (Host, i, _TOKEN)).json()
                # print sites['msg']
                if str(sites['status']).lower() == 'false' or 'data' not in sites:
                    break

                for site in sites['data']:
                    if site['domain'] not in Sites:
                        Sites.append(site['domain'])

                time.sleep(0.5)
                i += 1

    print '[+]Sites(%d)' % len(Sites)
    if len(Sites) and s:
        print '  [-] ' + '\n  [-] '.join(Sites)
    print

    return Sites


# search('125.77.198.149')
