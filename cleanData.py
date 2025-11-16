import json
import pandas as pd
import datetime
import numpy as np
from collections import defaultdict

'''
The Big TODO:

create data sifting algorithm where the core loop does the following:
- iterate through all stopIDs and check for new stop times 
- on new stop detected store wait time in minutes and update last stop time FOR EACH TRAIN LINE AND DIRECTION 
- grab next diff, apply, and repeat

'''

with open('media/initial_data_20251111_030908.json', 'r') as file:
    data = json.load(file)


data = data['80']
def get_trips(data):
    trips = []
    for trip in data:
        tripData = {}
        tripData['tripId'] = trip['trip']['tripId']
        tripData['routeId'] = trip['trip']['routeId']
        tripData['directionId'] = trip['trip']['directionId']
        tripData['timestamp'] = datetime.datetime.fromtimestamp(int(trip['timestamp']))
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
    return df



def get_station_data(df):
    TrainStations = {}
    data = []
    df = df.drop_duplicates()
    df = df.sort_values(by='arrivalTime')
    df = df.dropna()
    for index, stop in df.iterrows():
        stopId = stop['stopId']
        route = stop['routeId']
        direction = stop['directionId']
        waitTime = -1
        arrivalTime = stop['arrivalTime']
        prevStop = None
        if stopId in TrainStations.keys():
            print('got stop')
            if route in TrainStations[stopId].keys():
                if direction in TrainStations[stopId][route].keys():
                    print('in the zone')
                    #both exist already, append and update
                    prevStop = TrainStations[stopId][route][direction][1]
                    waitTime = prevStop - stop['arrivalTime']
                    TrainStations[stopId][route][direction][0].append(waitTime)
                    TrainStations[stopId][route][direction][1] = stop['arrivalTime']
                else:
                    #stop and route, no direction
                    TrainStations[stopId][route][direction] = [[-1], stop['arrivalTime']]
            else:
                #stop but no route
                TrainStations[stopId][route] = {direction : [[-1], stop['arrivalTime']]}
        else:
            #nothing stored, add it all
            TrainStations[stopId] = {route : {direction : [[-1], stop['arrivalTime']]}}
        #add data to dataframe list
        keys = ['stopId', 'routeId', 'directionId', 'previousStop', 'thisStop', 'waitTime']
        values = [stopId, route, direction, prevStop, arrivalTime, waitTime]
        data.append(dict(zip(keys, values)))
    print(TrainStations)
    return pd.DataFrame(data)    

def data_loop():
    #load data

    #do the thing
    df = get_trips(data)
    df = get_station_data(df)
    print(df.to_string())  

    #update data with diff 


