import logging
import config
import re
from xbase import XBase
from datetime import timedelta
from datetime import datetime
from db import DB

class XPriceHistory(XBase):
    def __init__(self):
        super(XPriceHistory, self).__init__()
        self.db=DB()
        self.days=[]
        self.ranges =[]
        for i in self.cfg.readlines():
            i = i.rstrip()
            if i:
                print "%s"%i
                (day,value) = i.split("=")
                self.days.append(timedelta(days=int(day)))
                self.ranges.append([int(x) for x in value.split(',')])
    def filter(self,strs):
        return True

    def format(self,str_list):
        """
        str_list symbol date ....
        format return list[x1,x2,x3...]
        """
        rlist=[]
        if(not self.filter(str_list)):
            return None

        symbol=str_list[0]
        date = str_list[1]
        current = self.db.get_pre(symbol,date)
        if None == current:
            logging.error("No current data symbol %s date %s"%(symbol,date))
            return None

        i = 0
        for days_interval in self.days:
            pre_day = date - days_interval
            pre_one = self.db.get_pre(symbol, pre_day)

            if None == pre_one:
                logging.error("No next one data symbol %s date %s, pre_day %s"%(symbol,date,pre_day))
                return None

            # long time no trade
            if(date  - pre_one[1] >
                   (days_interval*2 if days_interval > timedelta(days=2) else timedelta(days=3))):
                logging.error("Too long before trade symbol %s date %s, pre_day %s\n current %s \n pre one%s " %
                              (symbol,date,pre_day,current,pre_one))
                return None

            perfor = self.get_performance(pre_one,current,self.ranges[i])
            rlist.append(perfor)
            i = i+1

        return rlist

    def get_performance(self, pre, next_one,criteria):
        a = 100*(next_one[7] - pre[7])//pre[7]
        for i in range(0,len(criteria)):
            if a < criteria[i]:
                return i
        return len(criteria)

