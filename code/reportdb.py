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
from getdata.crawl_report import getFieldsByPage

def init_logger():
    level = logging.ERROR
    if config.DEBUG:
        level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(filename)s: %(lineno)d: [%(levelname)s] %(message)s', level=level)

CREATE_TABLE="""
CREATE TABLE `stock`.`report` (
  `Symbol` VARCHAR(6) NOT NULL,
  `Date` DATE NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Title` VARCHAR(90) NOT NULL,
  `Industry` VARCHAR(45) NULL,
  `Broker` VARCHAR(45) NULL,
  `Reporter` VARCHAR(45) NOT NULL,
  `Rank` VARCHAR(45) NULL,
  `Action` VARCHAR(45) NULL,
  `Space` VARCHAR(45) NULL,
  PRIMARY KEY (`Symbol`, `Date`, `Title`, `Reporter`))
DEFAULT CHARACTER SET = utf8;
"""

INSERT_HISTORY="INSERT INTO report (Symbol,Date,Name,Title,Industry,Broker,Reporter,Rank,Action,Space) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
SELECT_HISTORY="SELECT * from report where Symbol='%s' and Date='%s'"
SELECT_HISTORY_RANGE="SELECT * from report where Symbol='%s' and Date>='%s' and Date<='%s'"
HISTORY_COUNT="SELECT count(*) from report where Symbol='%s' and Date='%s' and Title='%s' and Reporter='%s'"
SELECT_ALL_HISTORY="SELECT * from report Order by Date"
GET_LATEST_DATE="SELECT MAX(Date) from report"

class ReportDB():
    conn = pymysql.connect(host=config.host,
                           port=config.port,
                           user=config.user,
                           db=config.db,
                           passwd=config.passwd,
                           charset='utf8',
                           use_unicode=False)
    print("call when ReportDB init")

    def __init__(self):
        self.cur = self.conn.cursor()
   
    def execute(self,s):
        logging.debug(s)
        self.cur.execute(s)

    def fetchone(self):
        return self.cur.fetchone()

    def execute_get_all(self):
        self.execute(SELECT_ALL_HISTORY)

    def commit(self):
        self.conn.commit()

    def create_table(self):
        self.execute(CREATE_TABLE)

    def get_latest_date(self):
        self.execute(GET_LATEST_DATE)
        return self.cur.fetchone()

    def insert_history(self,Symbol,Date,Name,Title,Industry,Broker,Reporter,Rank,Action,Space):
        self.execute(INSERT_HISTORY%(Symbol,Date,Name,Title,Industry,Broker,Reporter,Rank,Action,Space))

    def get_history(self,symbol,time):
        self.execute(SELECT_HISTORY%(symbol,time))
        return self.cur.fetchone()

    def get_count(self,symbol,time,title,reporter):
        self.execute(HISTORY_COUNT%(symbol,time,title,reporter))
        return self.cur.fetchone()

    def get_one(self,symbol,time_from, time_to):
        self.execute(SELECT_HISTORY_RANGE%(symbol,time_from, time_to))
        return self.cur.fetchone()

    def get_many(self,symbol,time_from, time_to):
        self.execute(SELECT_HISTORY_RANGE%(symbol,time_from, time_to))
        return self.cur.fetchall()

    def __is_equal(self,a, b, absError=0.0001):
        if (abs(a-b) <= max(abs(a), abs(b))*absError ):
            return True
        else:
            return False

    def close(self):
        self.commit()
        self.cur.close()
        self.conn.close()

    def filter(self,strs):
        if 10 != len(strs):
            logging.error("skip one line lenght not right")
            [logging.error(i.decode('utf-8')) for i in strs]
            return False
        else:
            exist_count = int(self.get_count(strs[1],strs[0],strs[3],strs[6])[0])
            pattern = re.compile(r'\d{6}')
            if exist_count > 0:
                logging.error("duplicate line %s"%exist_count)
                [logging.error(i.decode('utf-8')) for i in strs]
                return False
            elif not pattern.match(strs[1]):
                logging.error("dirty line")
                [logging.error(i.decode('utf-8')) for i in strs]
                return False
            return True

    def insert_history_from_file(self):
      with open(config.REPORT_FILE, "r") as f:
        for line in f:
          line = line.rstrip()
          array = re.split(r'\t', line)
          #[logging.error(i.decode('utf-8')) for i in array]

          if not self.filter(array):
              continue

          self.insert_history(array[1],array[0],
                              array[2],array[3],
                              array[4],
                              array[5],array[6],
                              array[7],array[8],
                              array[9])

      self.commit()

    def update_history(self):
        latest_date= self.get_latest_date()
        if None == latest_date:
            logging.error("Is this your first time using this DB? if not something wrong, if yes remove following comment")
            #latest_date = datetime.strptime('1989-01-01','%Y-%m-%d');
            return
        else:
            latest_date = latest_date[0]

        should_be_true = True
        page = 1
        while should_be_true:
            fieldRows = getFieldsByPage(page)
            logging.debug('page %s count: %s'%(page,len(fieldRows)))
            if(len(fieldRows) < 1):
                logging.error("Something wrong with get page will not commit to DB")
                return

            for fieldRow in fieldRows:
                fields =[fieldRow[-1]]
                fields.extend(fieldRow[0:-1])
                for i in range(0,len(fields)):
                    fields[i] = fields[i].encode("utf8")

                logging.debug(fields)
                this_date = datetime.strptime(fields[0],'%Y-%m-%d').date()
                # get more days of report for tolerate
                if this_date < latest_date - timedelta(days=config.TOLERATE_DAYS):
                    should_be_true = False
                if not self.filter(fields):
                    continue
                self.insert_history(*fields)

            page = page+1

        self.commit()


if __name__ == "__main__":
    init_logger()
    db=ReportDB()
    #db.create_table()
    db.update_history()
    db.close()
