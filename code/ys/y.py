import logging
from db import DB
from datetime import timedelta
from datetime import datetime

class Y(object):
    def __init__(self, interval):
        self.db=DB()
        self.set_interval(interval)
        logging.debug("init y %s"%self.__class__.__name__)

    def set_interval(self, interval):
        self.interval = interval
        self.days_interval = timedelta(days=interval)
        logging.debug("set interval %s"%self.days_interval)


    ## Abstract methods
    def calculate(self,vlist):
        """
        calculate vlist=['symbol','date',[]]
        return vlist=performance
        """
        pass


