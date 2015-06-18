import logging
import config
import re
from xbase import XBase
from datetime import timedelta
from datetime import datetime
from db import DB
from .xpricehistory import XPriceHistory

class XVolumeHistory(XBase):
  def __init__(self):
    super(XVolumeHistory, self).__init__()

    self.db=DB()
    self.days =[]
    self.ranges =[]

    smooth_days=self.cfg.readline()
    self.smooth_days = int(smooth_days)
    for i in self.cfg.readlines():
      i = i.rstrip()
      if i:
        print "i%s"%i
        (day,value) = i.split("=")
        self.days.append(timedelta(days=int(day)))
        self.ranges.append([int(x) for x in value.split(',')])

  def filter(self,strs):
    return True

  def format(self,line):
    """
    format return list[x1,x2,x3...]
    """
    rlist=[]
    vlist = re.split(r'\t', line)
    if(not self.filter(vlist)):
      return None

    symbol=vlist[1]
    date_time=datetime.strptime(vlist[0],'%Y-%m-%d')
    current_n = self.db.get_pre_many(symbol,date_time.date(),self.smooth_days)
    if self.smooth_days != len(current_n):
      logging.error("No data")
      return None

    i = 0
    for days_interval in self.days:
      pre_day = date_time - days_interval
      pre_n = self.db.get_pre_many(symbol, pre_day.date(),self.smooth_days)

      if self.smooth_days != len(pre_n):
        logging.error("No next one data")
        return None

      # long time no trade
      if(date_time.date() - pre_n[-1][1] >
          ((days_interval + timedelta(days=self.smooth_days-1))*2 if (days_interval + timedelta(days=self.smooth_days-1)) > timedelta(days=2) else timedelta(days=3))):
        logging.error("Too long before trade\nnow %s \n pre one%s "%(current_n[0],pre_n[0]))
        return None

      perfor = self.get_performance(pre_n,current_n,self.ranges[i],self.smooth_days)
      rlist.append(perfor)
      i = i+1

    return rlist

  def get_performance(self, pre_n, next_n,criteria,n):

    pre=0
    nxt=0
    for i in range(0,n):
        pre = pre + pre_n[i][6]
        nxt = nxt + next_n[i][6]

    a = 100*(nxt - pre)//pre

    for i in range(0,len(criteria)):
      if a < criteria[i]:
        return i
    return len(criteria)

