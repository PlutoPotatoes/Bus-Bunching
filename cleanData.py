import json
import pandas as pd
import datetime

with open('startData2.json', 'r') as file:
    data = json.load(file)

data = data['4']
trips = []
for trip in data:
    tripData = {}
    tripData['tripId'] = trip['trip']['tripId']
    tripData['routeId'] = trip['trip']['routeId']
    tripData['directionId'] = trip['trip']['directionId']
    tripData['timestamp'] = trip['timestamp']
    if('vehicle' in trip.keys()):
        tripData['vehicleId'] = trip['vehicle']['id']
    for update in trip['stopTimeUpdate']:
        tripData['stopSequence'] = update['stopSequence']
        tripData['stopId'] = update['stopId']
        if('arrival' in update.keys()):
            time = datetime.datetime.fromtimestamp(int(update['arrival']['time']))
            tripData['arrivalTime'] = time
            tripData['departureTime'] = ''

        if('departure' in update.keys()):
            tripData['departureTime'] = datetime.datetime.fromtimestamp(int(update['departure']['time']))
        trips.append(tripData)
        
df = pd.DataFrame(trips)
print(df[df['tripId'] == '10004003782813-JUNE25'].to_string())

