import json
import pandas as pd
import datetime

with open('initial_data.json', 'r') as file:
    data = json.load(file)

data = data['207']
trips = []
for trip in data:
    tripData = {}
    tripData['tripId'] = trip['trip']['tripId']
    tripData['routeId'] = trip['trip']['routeId']
    tripData['directionId'] = trip['trip']['directionId']
    tripData['timestamp'] = trip['timestamp']
    for update in trip['stopTimeUpdate']:
        tripData['stopSequence'] = update['stopSequence']
        tripData['stopId'] = update['stopId']
        if('arrival' in update.keys()):
            time = datetime.datetime.fromtimestamp(int(update['arrival']['time']))
            tripData['arrivalTime'] = time
            tripData['departureTime'] = ''

        else:
            tripData['arrivalTime'] = ''
            tripData['departureTime'] = update['departure']['time']
        trips.append(tripData)
        
df = pd.DataFrame(trips)
print(df.drop_duplicates())

