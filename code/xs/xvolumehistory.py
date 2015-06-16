import logging
import config
import re
from xbase import XBase
from datetime import timedelta
from datetime import datetime
from db import DB
from .xpricehistory import XPriceHistory

class XVolumeHistory(XPriceHistory):
  def __init__(self):
    super(XVolumeHistory, self).__init__()

  def get_performance(self, pre, next_one,criteria):
    a = 100*(next_one[6] - pre[6])//pre[6]
    for i in range(0,len(criteria)):
      if a < criteria[i]:
        return i
    return len(criteria)

