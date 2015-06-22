import logging
import config
import re
from xbase import XBase
from datetime import timedelta
from datetime import datetime
from reportdb import ReportDB
from .x1formater import X1Formater

class XN(XBase):
    def __init__(self):
        super(XN, self).__init__()
        self.db=ReportDB()

        self.days_list =[]
        for i in self.cfg.readline().split(" "):
            self.days_list.append(timedelta(days=int(i)))

        print(self.days_list)
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

        print(self.x_formater_list)

    def get_formater(self, name):
        exec('import x1f' + name.lower())
        f = eval('x1f%s.X1F%s()'%(name.lower(), name))
        return f

    def filter(self,strs):
        return True

    def format(self,str_list):
        """
        str_list symbol date ....
        format return list[x1,x2,x3...]
        """
        rlist=[]
        if(not self.filter(str_list)):
            return None

        symbol = str_list[0]
        date = str_list[1]

        for days in self.days_list:
            pre_date = date - days

            report_list_list = self.db.get_many_in_range(symbol,pre_date,date)
            #logging.error(report_list_list)
            # how many reports
            rlist.append(len(report_list_list))

            x_list_list_list = [[] for x in range(0,self.line_number)]

            for str_list_ in report_list_list:
                i=0
                for s in str_list_[2:]:
                    if self.x_formater_list[i] != None:
                        ls = self.x_formater_list[i].format(s)
                        if None != ls:
                            x_list_list_list[i].append(ls)
                    i = i + 1;

            i=0
            for i in range(0, len(self.x_formater_list)):
                if self.x_formater_list[i] != None:
                    if(0 == len(x_list_list_list[i])):
                        return None

                    agg_x_list = [ 0 for x in range(0,len(x_list_list_list[i][0]))]
                    for x_list in x_list_list_list[i]:
                        func = lambda x,y : float(x)+float(y)
                        agg_x_list = map(func,agg_x_list,x_list)

                    rlist.append(len(x_list_list_list[i]))
                    for agg in agg_x_list:
                        rlist.append(round(float(agg/len(x_list_list_list[i])),2))

        return rlist


