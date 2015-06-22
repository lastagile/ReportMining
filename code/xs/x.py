import logging
import config
import re
from reportdb import ReportDB
from datetime import datetime,timedelta

class X(object):  
  def __init__(self): 
    logging.debug("init x to %s"%self.__class__.__name__)
    self.xobj_list = []
    self.init_x(config.x)
    self.db = ReportDB()
    from_day = datetime.strptime(config.FROM_DAY,'%Y-%m-%d').date()
    to_day = datetime.strptime(config.TO_DAY,'%Y-%m-%d').date()
    self.db.execute_get_many_in_range(from_day,to_day,config.READ_FORWARD)


  def read_line(self):
      while True:
        line = self.db.fetchone()
        if ( None == line ):
          return None
        else:
          logging.debug(line)
          a = self.format(line)
          if a:
              return a

  def init_x(self, x_list):
    for x in x_list: 
      exec('import ' + x.lower())
      x_obj = eval(x.lower() + '.' + x + '()')
      self.xobj_list.append(x_obj)

  def format(self,str_list):
    """
    format return symbol, date, list[x1,x2,x3...]
    """
    x_list = []
    for x_obj in self.xobj_list:
      x1_list = x_obj.format(str_list)
      if None == x1_list:
        return None

      for x in x1_list: 
        x_list.append(x)

    return (str_list[0],str_list[1],x_list)

