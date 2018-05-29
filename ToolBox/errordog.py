# -*- coding: utf-8 -*-
import traceback
from ToolBox.putColor import *


class ErrorDog:
    def __init__(self, api_name):
        self.log = 'log.here'
        self.api_name = api_name

    def __call__(self, func):
        def inside(Host, s):
            try:
                return func(Host, s)
            except Exception, e:
                if 'Keyboard' not in str(e):
                    with open(self.log, 'a') as fp:
                        fp.write(traceback.format_exc()+'\n'+'-'*50 + '\n')

                    print "[X]"+putColor("The api of %s was broken. Check the log in %s\n" %
                                         (self.api_name, self.log), 'red')
                return []
        return inside
