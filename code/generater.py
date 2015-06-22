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
        sub_str=""
        if config.PREDICT:
            sub_str = ".pre"
        wf_name = datetime.now().strftime('%Y-%m-%d.%H-%M-%S')
        call(["rm", "-f", "../output/current%s.txt"%sub_str])
        call(["touch", "../output/%s%s.txt"%(wf_name,sub_str)])
        call(["ln", "-s", "../output/%s%s.txt"%(wf_name,sub_str), "../output/current%s.txt"%(sub_str)])
        wf = open("../output/%s%s.txt"%(wf_name,sub_str), 'w')

        a=self.x.read_line()
        logging.debug(a)
        while a:
            if config.PREDICT:
                y = -1
            else:
                y = self.y.calculate(a)
            if None != y :
                output = "%s\t%s\t%s\t%s\n"%(a[1], a[0], y, '\t'.join([str(x) for x in a[2]]))
                # ['date','symbol',performance,[]]
                logging.debug(output)
                wf.write(output)

            a=self.x.read_line()
            logging.debug(a)

        wf.close()
        logging.debug("run end...")


