import DataCollection

#all bus routes with average daily ridership >15,000 over the past year
#https://ridership.streetsforall.org/
routes = ['2','4','16','18','33','51','70','240','251','720','754']


DataCollection.diffUpdates(routes, interval=5)