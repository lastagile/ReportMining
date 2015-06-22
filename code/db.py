#!/usr/local/bin/python

import logging
import time
import base64
import hmac
import hashlib
import sys
import config
import hashlib
from datetime import datetime,timedelta
import re
import time
import pymysql
from getdata.gen_symbol_list import excractSymbolList
from getdata.crawl_price_in_yahoo import genPricesBySymbol,genPricesProvideSymbol

def init_logger():
    level = logging.ERROR
    if config.DEBUG:
        level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(filename)s: %(lineno)d: [%(levelname)s] %(message)s', level=level)

CREATE_TABLE="""
CREATE TABLE `stock`.`price` (
  `Symbol` VARCHAR(6) NOT NULL,
  `Date` DATE NOT NULL,
  `Open` FLOAT NULL,
  `High` FLOAT NULL,
  `Low` FLOAT NULL,
  `Close` FLOAT NULL,
  `Volume` BIGINT NULL,
  `AdjClose` FLOAT NULL,
  PRIMARY KEY (`Symbol`, `Date`));
"""

INSERT_HISTORY="INSERT INTO price (Symbol,Date,Open,High,Low,Close,Volume,AdjClose) VALUES('%s','%s',%s,%s,%s,%s,%s,%s)"
SELECT_HISTORY="SELECT * from price where Symbol='%s' and Date='%s'"
SELECT_NEXT_N="SELECT * from price where Symbol='%s' and Date>='%s' and Volume!=0 Order by Date Limit %s"
SELECT_PRE_N="SELECT * from price where Symbol='%s' and Date<='%s' and Volume!=0 Order by Date DESC Limit %s"
HISTORY_COUNT="SELECT count(*) from price where Symbol='%s' and Date='%s'"
GET_LATEST_DATE="SELECT MAX(Date) from price where Symbol='%s'"
SELECT_HISTORY_RANGE="SELECT * from price where Symbol='%s' and Date>='%s' and Date<='%s' Order by Date"
GET_LATEST_DATE_BEFORE="SELECT MAX(Date) from price where Symbol='%s' and Date<='%s'"

class DB():
    conn = pymysql.connect(host=config.host,port=config.port,user=config.user,db=config.db,passwd=config.passwd)
    print("call when DB init")

    def __init__(self,):
        self.cur=self.conn.cursor()
   
    def execute(self,s):
        logging.debug(s)
        self.cur.execute(s)

    def fetchone(self):
        return self.cur.fetchone()

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.execute(CREATE_TABLE)

    def insert_history(self,Symbol,Date,Open,High,Low,Close,Volume,AdjClose):
        self.execute(INSERT_HISTORY%(Symbol,Date,Open,High,Low,Close,Volume,AdjClose))


    def get_history(self,symbol,time):
      self.execute(SELECT_HISTORY%(symbol,time))
      return self.cur.fetchone()

    def get_next(self,symbol,time):
      self.execute(SELECT_NEXT_N%(symbol,time,1))
      return self.cur.fetchone()

    def get_pre(self,symbol,time):
      self.execute(SELECT_PRE_N%(symbol,time,1))
      return self.cur.fetchone()

    def get_pre_many(self,symbol,time,n):
      self.execute(SELECT_PRE_N%(symbol,time,n))
      return self.cur.fetchall()

    def get_next_many(self,symbol,time,n):
      self.execute(SELECT_NEXT_N%(symbol,time,n))
      return self.cur.fetchall()

    def get_latest_date(self,symbol,date=datetime.now().date()):
        self.execute(GET_LATEST_DATE_BEFORE%(symbol,date))
        return self.cur.fetchone()

    def get_range(self,symbol,from_day,to_day):
        self.execute(SELECT_HISTORY_RANGE%(symbol,from_day,to_day))
        return self.cur.fetchall()

    def get_count(self,symbol,time):
        self.execute(HISTORY_COUNT%(symbol,time))
        return self.cur.fetchone()

    def __is_equal(self,a, b, absError=0.0001):
        if (abs(a-b) <= max(abs(a), abs(b))*absError ):
            return True
        else:
            return False

    def close(self):
        self.commit()
        self.cur.close()

    def date_clean(self,symbol,from_day,to_day):
        values = self.get_range(symbol,from_day,to_day)
        pre_day=values[0]
        for next_day in values[1:]:
            two_day_per = 100*( next_day[7] - pre_day[7] ) / pre_day[7]
            if(abs(two_day_per) > config.DIRTY_RANGE):
                logging.error("date_clean Dirty data:\n pre_day %s \n next_day%s "%(pre_day,next_day))
                return False
            pre_day = next_day

        return True

    def update_history_from_file(self):
      count = 0
      with open(config.PRICE_FILE, "r") as f:
        for line in f:
          array = line.split()
          exist_count = int(self.get_count(array[0],array[1])[0])
          if exist_count > 0:
              logging.error("duplicate line %s"%count)
              logging.error(line)
              continue

          logging.error(array)
          self.insert_history(array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7])
          if count > 1000:
            self.commit()
            count = 0
            logging.info('insert 1000')
          else:
            count = count + 1

      self.commit()

    def update_history_index_from_file(self):
      count = 0
      with open(config.SHA_INDEX_FILE, "r") as f:
        for line in f:
          array = line.split(',')
          exist_count = int(self.get_count('000000',array[0])[0])
          if exist_count > 0:
              logging.error("duplicate line %s"%count)
              logging.error(line)
              continue
          self.insert_history('000000',array[0],array[1],array[2],array[3],array[4],array[5],array[6])
          if count > 1000:
            self.commit()
            count = 0
            logging.info('insert 1000')
          else:
            count = count + 1

      self.commit()

    def update_history(self):
        #for console
        symbolListFile = config.SYMBOL_List_FILE
        symbolList = excractSymbolList(symbolListFile)
        for symbol in symbolList:
            latest = self.get_latest_date(symbol)
            if None == latest[0]:
                prices = genPricesBySymbol(symbol)
            else:
                # set days - TOLERATE_DAYS so that we can bypass some error case of last time update
                prices = genPricesBySymbol(symbol,latest[0]-timedelta(days=config.TOLERATE_DAYS))

            logging.debug(symbol + ' count:' + str(len(prices)))
            for priceOnDay in prices:
                if int(self.get_count(symbol,priceOnDay[0])[0]) > 0:
                    logging.error("duplicate line")
                    logging.error(priceOnDay)
                    continue
                self.insert_history(symbol,*priceOnDay)

            self.commit()

    def update_index_history(self):
        #for console
        url_symbol = '000001.SS'
        symbol = '000000'
        latest = self.get_latest_date(symbol)
        if None == latest[0]:
            prices = genPricesBySymbol(symbol)
        else:
            # set days - TOLERATE_DAYS so that we can bypass some error case of last time update
            prices = genPricesProvideSymbol(url_symbol,latest[0]-timedelta(days=config.TOLERATE_DAYS))

        logging.debug(symbol + ' count:' + str(len(prices)))
        for priceOnDay in prices:
            if int(self.get_count(symbol,priceOnDay[0])[0]) > 0:
                logging.error("duplicate line")
                logging.error(priceOnDay)
                continue
            self.insert_history(symbol,*priceOnDay)

        self.commit()

if __name__ == "__main__":
    init_logger()
    db=DB()
    #db.create_table()
    #db.update_history_from_file()
    #db.update_history_index_from_file()
    db.update_history()
    db.update_index_history()
    db.close()
