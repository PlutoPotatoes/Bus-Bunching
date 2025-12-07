import csv

routescsv = 'routenames.csv'
stopscsv = 'stopnames.csv'

routes = {}
stops = {}

with open(routescsv, mode ='r')as file:
    csvreader = csv.reader(file)
    cols = next(csvreader)
    for row in csvreader:
        routeID = row[0]
        routeName = row[2]
        bgcolor = row[5]
        txtcolor = row[6]
        routes[routeID] = {
            'name': routeName,
            'bgcolor': tuple(int(bgcolor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)),
            'txtcolor': tuple(int(txtcolor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        }

with open(stopscsv, mode ='r')as file:
    csvreader = csv.reader(file)
    cols = next(csvreader)
    for row in csvreader:
        stopID = row[0]
        stopName = row[2]
        stopLat = row[4]
        stopLon = row[5]
        stops[stopID] = {
            'name': stopName,
            'lat': stopLat,
            'lon': stopLon
        }
        
def routeIDtoName(routeID):
    return routes[routeID]['name']

    
def stopIDtoName(stopID):
    if stopID in stops:
        return stops[stopID]['name']
    else:
        return "Unknown Stop"