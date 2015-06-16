import logging
import config
import re


class X1Formater():
  ## Abstract methods 
  def format(self,line):
    """
    format return list[x1,x2,x3...]
    """
    return []


