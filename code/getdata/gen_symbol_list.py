
import codecs


def excractSymbolList(symbolListFile):
    symbolList = []
    for line in codecs.open(symbolListFile, 'r', 'utf-8'):
        symbol = line.rstrip('\n').split('\t')[0]
        symbolList.append(symbol)
    return symbolList

def validation(fieldType, numTokens):
    if fieldType == 'profit' and numTokens == 5 + 7:
        return True
    elif fieldType == 'operation' and numTokens == 5 + 6:
        return True
    elif fieldType == 'grow' and numTokens == 5 + 6:
        return True
    elif fieldType == 'debtpaying' and numTokens == 5 + 6:
        return True
    elif fieldType == 'cashflow' and numTokens == 5 + 5:
        return True
    elif fieldType == 'mainindex' and numTokens == 5 + 10:
        return True
    elif fieldType == 'news' and numTokens == 5 + 9:
        return True
    else:
        return False


if __name__ == '__main__':

    intputFile = '../data/finance.1104.data'
    outputFile = '../data/symbolList.1105.data.2'

    symbolSet = set()
    cnt = 1
    for line in codecs.open(intputFile, 'r', 'utf-8'):
        line = line.rstrip('\n')
        tokens = line.split('\t')
        #validation
        fieldType, symbol, name = tokens[0], tokens[3], tokens[4]
        if not validation(fieldType, len(tokens)):
            print 'not valid: ' + line
            raise RuntimeError

        cnt += 1
        if cnt % 10000 == 0:
            print 'line ' + str(cnt)
        symbolSet.add(symbol + '\t' + name)

    writer = codecs.open(outputFile, 'w', 'utf-8')
    for symbol in sorted(symbolSet):
        writer.write("%s\n" % symbol)
    writer.close()