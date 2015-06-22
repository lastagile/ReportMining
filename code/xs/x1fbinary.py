import logging
import config
import re

from x1formater import X1Formater

class X1FBinary(X1Formater):

    def init(self,strs):
        self.s_list = strs.split()[1:]
        logging.debug(self.s_list)

    def format(self,strs):
        rt=[]
        for i in self.s_list:
            if i == strs:
                rt.append(1)
            else:
                rt.append(0)

        if len(rt):
            return rt
        else:
            return None
