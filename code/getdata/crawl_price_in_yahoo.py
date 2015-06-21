# -*- coding: utf-8 -*-

from urllib import urlopen
import codecs
import time
import socket
import urllib2
from datetime import datetime,timedelta
import config
import gen_symbol_list


socket.setdefaulttimeout(5) #set time out for urlopen

#watch out for bug, some symbol won't get the csv files
# http://real-chart.finance.yahoo.com/table.csv?s=600893.SS&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv
# http://real-chart.finance.yahoo.com/table.csv?s=601008.SS&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv
# http://real-chart.finance.yahoo.com/table.csv?s=603606.SS&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv

# http://real-chart.finance.yahoo.com/table.csv?s=000001.SS&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv
# http://real-chart.finance.yahoo.com/table.csv?s=002009.SZ&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv
# http://real-chart.finance.yahoo.com/table.csv?s=300399.SZ&d=11&e=31&f=2014&g=d&a=00&b=01&c=1989&ignore=.csv

# index
#http://real-chart.finance.yahoo.com/table.csv?s=000001.SS&d=11&e=31&f=2015&g=d&a=00&b=01&c=1989&ignore=.csv
#error symbol: 002160 and lost of ot:hers


def genPricesBySymbol(symbol,date_from=datetime.strptime('1989-01-01','%Y-%m-%d').date(),date_to=datetime.now().date()):
    if symbol.startswith('600') or symbol.startswith('601') or symbol.startswith('603'):
        symbol = symbol + '.SS'
    elif symbol.startswith('000') or symbol.startswith('002') or symbol.startswith('300'):
        symbol = symbol + '.SZ'
    else:
        return []
    #from 1989.01.01 - 2014.12.31
    url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%s&e=%s&f=%s&g=d&a=%s&b=%s&c=%s&ignore=.csv'\
          %(symbol,date_to.month - 1, date_to.day,date_to.year,date_from.month-1,date_from.day,date_from.year)
    print url
    return genPricesBySymbol_helper(url)


def genPricesProvideSymbol(symbol,date_from=datetime.strptime('1989-01-01','%Y-%m-%d'),date_to=datetime.now().date()):

    #from 1989.01.01 - 2014.12.31
    url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%s&e=%s&f=%s&g=d&a=%s&b=%s&c=%s&ignore=.csv'\
          %(symbol,date_to.month - 1, date_to.day,date_to.year,date_from.month-1,date_from.day,date_from.year)
    print url
    return genPricesBySymbol_helper(url)

def genPricesBySymbol_helper(url):

    flagHasTobeTrue = False
    times = 0
    while not flagHasTobeTrue:
        if times > config.NET_WORK_RETRY_TIMES:
            return []
        times = times + 1

        try:
            response = urllib2.urlopen(url, timeout = 10)
            code = response.getcode()
            if code != 200:
                print('code != 200' + 'retry ' + url)
                continue
            text = response.read()
            lines = text.split('\n')

            flagHasTobeTrue = True
        except Exception, e:
            print e
            time.sleep(2)
            print 'retry ' + url

    prices = []
    for line in lines[1:]:  #drop the header
        if line.strip() == '':
            continue
        priceOneDay = []
        for token in line.split(','):
            priceOneDay.append(token)
        prices.append(priceOneDay)
    prices.reverse()
    return prices

if __name__ == '__main__':
    # symbolListFile = '../data/symbolList.1105.data'
    # priceFile = '../data/price.1205.yahoo.data'

    #for console
    symbolListFile = '../../data/symbolList.1105.data.small'
    priceFile = '../../data/price.0620.yahoo.data'

    writer = codecs.open(priceFile, 'w', 'utf-8')

    symbolList = gen_symbol_list.excractSymbolList(symbolListFile)

    for symbol in symbolList:
        prices = genPricesBySymbol(symbol)
        print symbol, 'count:' + str(len(prices))
        for priceOnDay in prices:
            writer.write("%s\t%s\n" % (symbol, '\t'.join(priceOnDay)))
        time.sleep(0.2)
    writer.close()