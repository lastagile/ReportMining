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

def init_logger(level = logging.INFO):
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
SELECT_PRE_N="SELECT * from price where Symbol='%s' and Date<='%s' and Volume!=0 Order by Date Limit %s"


class DB():
    def __init__(self,host='127.0.0.1',port=3306,user='root',db='stock',passwd=''):
        self.conn = pymysql.connect(host=host,port=port,user=user,db=db,passwd=passwd)
        self.cur=self.conn.cursor()
   
    def execute(self,s):
        logging.debug(s)
        self.cur.execute(s)

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

    def get_pre_pirce(self,symbol,time):
      self.execute(SELECT_PRE_N%(symbol,time,1))
      return self.cur.fetchone()

    def get_pre_many(self,symbol,time,n):
      self.execute(SELECT_PRE_N%(symbol,time,n))
      return self.cur.fetchmany(size=n)

    def get_pre_many(self,symbol,time,n):
      self.execute(SELECT_NEXT_N%(symbol,time,n))
      return self.cur.fetchmany(size=n)

    def __is_equal(self,a, b, absError=0.0001):
        if (abs(a-b) <= max(abs(a), abs(b))*absError ):
            return True
        else:
            return False

    def close(self):
        self.commit()
        self.cur.close()
        self.conn.close()

    def insert_history_all(self):
      count = 0
      with open(config.PRICE_FILE, "r") as f:
        for line in f:
          array = line.split()
          self.insert_history(array[0],array[1],array[2],array[3],array[4],array[5],array[6],array[7])
          if count > 1000:
            self.commit()
            count = 0
            logging.info('insert 1000')
          else:
            count = count + 1

      self.commit()

    def insert_history_index(self):
      count = 0
      with open(config.SHA_INDEX_FILE, "r") as f:
        for line in f:
          array = line.split(',')
          self.insert_history('000000',array[0],array[1],array[2],array[3],array[4],array[5],array[6])
          if count > 1000:
            self.commit()
            count = 0
            logging.info('insert 1000')
          else:
            count = count + 1

      self.commit()


if __name__ == "__main__":
    init_logger()
    db=DB()
    #db.create_table()
    #db.insert_history_all()
    db.insert_history_index()
    db.close()
