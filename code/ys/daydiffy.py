from .y import Y
import config
import logging
from datetime import timedelta
from datetime import datetime

class DayDiffY(Y):
  def __init__(self, days = config.days):
    super(DayDiffY, self).__init__(days)
    self.criteria=config.daydiffcriteria 

  def calculate(self,vlist):
    """
    calculate vlist=['symbol','date',[]]
    return performance
    """
    symbol=vlist[0]
    date_time=vlist[1]
    current = self.db.get_pre(symbol,date_time)
    if None == current:
      logging.error("No data")
      return None

    date_time += self.days_interval
    next_one = self.db.get_next(symbol, date_time)

    if None == next_one:
      logging.error("No next one data")
      return None

    # long time no trade
    if(next_one[1] - date_time >
          (self.days_interval*2 if self.days_interval > timedelta(days=2) else timedelta(days=3))):
      logging.error("Too long before trade\nnow %s \n next one%s \n next two %s"%(current,next_one,next_two))
      return None

    if self.db.date_clean(symbol,current[1],next_one[1]):
        return None

    return self.get_performance(current,next_one)

  def get_performance(self, current, next_one):
    a = 100*(next_one[7] - current[7])//current[7]
    for i in range(0,len(self.criteria)):
      if a < self.criteria[i]:
        return i
    return len(self.criteria)

