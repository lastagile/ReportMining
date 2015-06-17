#!/usr/local/bin/python

import ys
import config
import logging
import db
from datetime import datetime
from subprocess import call
from xs.x import X

class Generater():
    def __init__(self):
      self.init_y(config.y)
      self.init_x()

    def init_y(self, y):
      exec('import ys.' + y.lower())
      y = eval('ys.' + y.lower() + '.' + y + '()')
      self.y = y

    def init_x(self):
      self.x = X()

    def init_interval(self, interval):
      self.y.set_interval(interval)

    def run(self):
      logging.debug("run start...")
      wf_name = datetime.now().strftime('%Y-%m-%d.%H-%M-%S')
      call(["rm", "-f", "../output/current.txt"])
      call(["touch", "../output/%s.txt"%wf_name])
      call(["ln", "-s", "../output/%s.txt"%wf_name, "../output/current.txt"])
      wf = open("../output/%s.txt"%wf_name, 'w')
      a=self.x.read_line()
      logging.debug(a)
      while a:
        y=self.y.calculate(a)
        if None != y :
          output = "%s\t%s\t%s\t%s\n"%(a[0], a[1], y, '\t'.join([str(x) for x in a[2]]))
          wf.write(output)
        a=self.x.read_line() 
        logging.debug(a)
        
      
      wf.close()
      logging.debug("run end...")


