PRICE_FILE="../data/1205.price.yahoo"
SHA_INDEX_FILE="../data/price.SHA000001.data.csv"
SHE_INDEX_FILE="../data/price.SHE399001.data.csv"

REPORT_FILE="../data/report.0428.1.data.small"
#REPORT_FILE="../data/report.0428.1.data.nodup"
read_forward="y"

y="AlphaDayDiffY"
daydiffcriteria = [-25,-10,-5,-2,0,2,5,10,25]
alphadaydiffcriteria = [-25,-10,-5,-2,0,2,5,10,25]
#x=["X1","XPriceHistory","AlphaXPriceHistory"]
x=["X1","AlphaXPriceHistory","XVolumeHistory"]
days=14
