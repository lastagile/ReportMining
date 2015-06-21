import logging
import config
import re

from x1formater import X1Formater

class X1FNumericRange(X1Formater):

  def __init__(self):
    self.i_range =[]

  def init(self,strs):
    a = strs.split()[1:]
    for i in a:
      self.i_range.append(float(i))

    logging.debug(self.i_range)

  def format(self,strs):
    rt=[]
    try:
      value = float(strs)
    except:
      logging.debug("no value")
      return None

    for i in range(0, len(self.i_range)):
      if(value < self.i_range[i]):
        rt.append(i)
        return rt

    rt.append(len(self.i_range))
    return rt


