import logging
import config
import re
from .x1formater import X1Formater
from xbase import XBase

class X1(XBase):
  def __init__(self):
    super(X1, self).__init__()

    self.line_number=int(self.cfg.readline())
    logging.debug(self.line_number)
    self.x_formater_list=[]
    for i in self.cfg.readlines():
      i = i.rstrip()
      if i:
        print "%s"%i
        formater= self.get_formater(i.split(" ")[0])
        formater.init(i)
        self.x_formater_list.append(formater)
      else:
         self.x_formater_list.append(None)

  def get_formater(self, name):
    exec('import x1f' + name.lower())
    f = eval('x1f%s.X1F%s()'%(name.lower(), name))
    return f

  def filter(self,strs):
    if self.line_number + 2 != len(strs):
      logging.error("skip one line lenght not right")
      [logging.error(i.decode('utf-8')) for i in strs]
      return False
    else:
      return True

  def format(self,str_list):
    """
    format return list[x1,x2,x3...]
    """
    xlist=[]
    if(not self.filter(str_list)):
      return None

    logging.debug(str_list)
    i=0
    for s in str_list[2:]:
      if self.x_formater_list[i] != None:
          ls = self.x_formater_list[i].format(s)
          logging.debug(ls)
          if None == ls:
            return None
          else:
            xlist.extend(ls)
      i = i + 1;
    return xlist
