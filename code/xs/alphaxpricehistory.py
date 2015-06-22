from .xpricehistory import XPriceHistory
import config
import logging
from datetime import timedelta
from datetime import datetime

class AlphaXPriceHistory(XPriceHistory):
    def __init__(self):
        super(AlphaXPriceHistory,self).__init__()

    def get_performance(self, current, next_one,criteria):

        index_current = self.db.get_history("000000",current[1])
        index_next_one = self.db.get_history("000000",next_one[1])

        if None == index_current or None == index_next_one:
            logging.error("No index data")
            return None

        a = 100*(next_one[7] - current[7])//current[7] - 100*(index_next_one[7] - index_current[7])//index_current[7]

        for i in range(0,len(criteria)):
            if a < criteria[i]:
                return i
        return len(criteria)

