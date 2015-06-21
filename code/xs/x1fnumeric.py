import logging
import config
import re

from x1formater import X1Formater

class X1FNumeric(X1Formater):

  def __init__(self):
    self.s_dict ={}
  def init(self,strs):
    a = strs.split()[1:]
    for i in a:
      (n,v) = i.split('=')
      self.s_dict[n] = v
    logging.debug(self.s_dict)

  def format(self,strs):
    if strs in self.s_dict:
      return [self.s_dict[strs]]
    else:
      return None

