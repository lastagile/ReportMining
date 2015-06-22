import logging
import config
import re

from x1formater import X1Formater

class X1FBinaryAgg(X1Formater):

    def init(self,strs):
        self.s_dict = {}
        a = strs.split()[1:]
        for i in a:
            (n,v) = i.split('=')
            self.s_dict[n] = v
        logging.debug(self.s_dict)

    def format(self,strs):
        rt=[]
        for i in range(0, len(self.s_dict)):
            rt.append(0)

        if strs in self.s_dict:
            rt[int(self.s_dict[strs]) - 1] = 1
            return rt
        else:
            return None

