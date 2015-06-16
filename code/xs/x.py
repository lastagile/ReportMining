import logging
import config
import re

class X(object):  
  def __init__(self): 
    logging.debug("init x to %s"%self.__class__.__name__)
    self.xobj_list = []
    self.init_x(config.x)
    self.f = open(config.REPORT_FILE, 'r')

  def read_line(self):
    if (config.read_forward == 'y'):
      while True:
        line = self.f.readline()
        if ( '' == line ):
          return None
        else:
          a = self.format(line)
          if a:
            return a
    else:
      logging.error("need to be done revert reading")

  def init_x(self, x_list):
    for x in x_list: 
      exec('import ' + x.lower())
      x_obj = eval(x.lower() + '.' + x + '()')
      self.xobj_list.append(x_obj)

  def format(self,line):
    """
    format return date, symbol, list[x1,x2,x3...]
    """
    x_list = []
    for x_obj in self.xobj_list:
      x1_list = x_obj.format(line)
      if None == x1_list:
        return None

      for x in x1_list: 
        x_list.append(x)

    strs = re.split(r'\t', line)
    return (strs[0],strs[1],x_list)

