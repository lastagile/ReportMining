# DB related
host='127.0.0.1'
port=3306
user='root'
db='stock'
passwd=''
MAX_MANY=10000

# file related
PRICE_FILE="../data/price.0620.yahoo.data.test"
SHA_INDEX_FILE="../data/2015-06-21 price.SHA000001.data.csv"
SHE_INDEX_FILE="../data/price.SHE399001.data.csv"

DEBUG=False
if DEBUG:
    REPORT_FILE="../data/report.0428.1.data.small"
    SYMBOL_List_FILE="../data/symbolList.1105.data.small"
else:
    REPORT_FILE="../data/report.0620.data.nodup"
    SYMBOL_List_FILE="../data/symbolList.1105.data"


NET_WORK_RETRY_TIMES = 10
TOLERATE_DAYS=30

# algos
read_forward="y"
y="AlphaDayDiffY"
daydiffcriteria = [-25,-10,-5,-2,0,2,5,10,25]
alphadaydiffcriteria = [-25,-10,-5,-2,0,2,5,10,25]
#x=["X1","XPriceHistory","AlphaXPriceHistory"]
x=["X1","AlphaXPriceHistory","XVolumeHistory","XN"]
#x=["XN"]
days=7

