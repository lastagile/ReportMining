from .y import Y
from .daydiffy import DayDiffY
import config
import logging
from datetime import timedelta
from datetime import datetime

class AlphaDayDiffY(DayDiffY):
  def __init__(self, days = config.days):
    super(AlphaDayDiffY, self).__init__(days)
    self.criteria=config.alphadaydiffcriteria 

  def get_performance(self, current, next_one):

    index_current = self.db.get_history_pirce("000000",current[1])
    index_next_one = self.db.get_history_pirce("000000",next_one[1])

    if None == index_current or None == index_next_one:
      logging.error("No index data")
      return None

    a = 100*(next_one[7] - current[7])//current[7] - 100*(index_next_one[7] - index_current[7])//index_current[7]

    for i in range(0,len(self.criteria)):
      if a < self.criteria[i]:
        return i
    return len(self.criteria)

