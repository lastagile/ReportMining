import logging
import config
import re

class XBase(object):
    def __init__(self):
        self.cfg = open("xs/%s.config"%self.__class__.__name__.lower(), 'r')
        logging.debug("init xBase %s"%self.__class__.__name__)

    def filter(self,str_list):
        return True

    def format(self,str_list):
        """
        str_list symbol date ....
        format return list[x1,x2,x3...]
        """
        xlist=[]
        if(not self.filter(str_list)):
            return None

        return xlist

