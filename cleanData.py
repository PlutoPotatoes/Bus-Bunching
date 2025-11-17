import json
import pandas as pd
import datetime
import numpy as np
from collections import defaultdict
import jsonpatch
from tqdm import tqdm

'''
The Big TODO:

create data sifting algorithm where the core loop does the following:
- iterate through all stopIDs and check for new stop times 
- on new stop detected store wait time in minutes and update last stop time FOR EACH TRAIN LINE AND DIRECTION 

'''

initial_data_path = 'media/initial_data_20251111_030908.json'
diff_data_path = 'data/diffs_20251111_030908.json'

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



def get_station_data(df, TrainStations):
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
            # print('got stop')
            if route in TrainStations[stopId].keys():
                if direction in TrainStations[stopId][route].keys():
                    # print('in the zone')
                    #both exist already, append and update
                    prevStop = TrainStations[stopId][route][direction][1]
                    waitTime = (stop['arrivalTime'] - prevStop).total_seconds() / 60
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
    # print(TrainStations)
    return TrainStations, pd.DataFrame(data)    

def data_loop(initial_data_path, diff_data_path, save_path):
    #load data
    with open(initial_data_path, 'r') as file:
        data = json.load(file)


    # data = data['80']

    TrainStations = {}

    #do the thing
    df = get_trips(data['80'])
    TrainStations, final_df = get_station_data(df, TrainStations)

    #update data with diff
    with open(diff_data_path, 'r') as file:
        diffs = file.readlines()
        
    for line in tqdm(diffs):
        timestamp, diff = line.split("\t", 1)
        patch = jsonpatch.JsonPatch.from_string(diff)
        data = patch.apply(data)
        df = get_trips(data['80'])
        TrainStations, df_new = get_station_data(df, TrainStations)
        final_df._append(df_new, ignore_index = True)


    final_df.sort_values(by='thisStop')
    final_df.to_csv(save_path)

    

    
    
data_loop('media/initial_data_20251111_030908.json', 'media/diffs_20251111_030908.json', 'station_data.csv')