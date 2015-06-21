# -*- coding: utf-8 -*-
import socket

from urllib2 import urlopen
import codecs
import time
import sys
import urllib2
from crawler.BeautifulSoup import BeautifulSoup


def getFieldsByPage(page):
    url = 'http://yanbao.stock.hexun.com/xgq/gsyj.aspx?1=1&page=' + str(page)
    print url

    timeout = 5
    socket.setdefaulttimeout(timeout)

    req_header = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }


    reports = []
    flagHasToBeTrue = False
    while not flagHasToBeTrue:
        try:
            #act as browser
            req_timeout = 5
            req = urllib2.Request(url,None,req_header)
            resp = urllib2.urlopen(req,None,req_timeout)
            code = resp.getcode()
            if code != 200:
                print('code != 200' + 'retry ' + url)
                continue

            text = resp.read()

            #old school
            # text = urlopen(url).read()

            #decode
            text = text.decode('gb18030') #can be used to handle gb2312

            soup = BeautifulSoup(text)
            dataTable = soup.find('table', width="100%")

            #drop first tr which is header
            trs = dataTable.findAll('tr', )[1:]
            flagHasToBeTrue = True
        except:
            time.sleep(2)
            print 'retry ' + url
            flagHasToBeTrue = False

    for tr in trs:
        report = []
        firstTd = tr.findAll('td',)[0]
        href = firstTd.findAll('a')[0]['href'][4:10]
        report.append(href)
        report.append(firstTd.text)
        for td in tr.findAll('td',)[1:]:
            report.append(td.text)
        reports.append(report)
    return reports

if __name__ == '__main__':

    outputFile = '../../data/report.0620.data'
    writer = codecs.open(outputFile, 'w', 'utf-8')

    for page in range(1, 3902):
        fieldRows = getFieldsByPage(page)
        print page, 'count:' + str(len(fieldRows))
        for fieldRow in fieldRows:
            writer.write('%s\t%s\n' % (fieldRow[-1], '\t'.join(fieldRow[:-1])))
        time.sleep(1)
        writer.flush()
    writer.close()

