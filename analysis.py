import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


bunchThreshold = 5.0

file = 'bunched_station_data_1.csv'
df = pd.read_csv(file, index_col=0)
df = df.drop_duplicates(subset=['vehicleId', 'stopId', 'directionId'])
df = df.sort_values(by=['stopSequence', 'directionId'], ignore_index=True)


RouteBunches = defaultdict(int)
StopBunches = defaultdict(int)
RouteTimelines = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
RouteBunchTimeline = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
#{routeId: {direction: {stopId: [waitTime/bunchNumber]}}



for route in df['routeId'].unique():
    for stationId in df["stopId"].unique():
        #mean = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].mean()
        #FIXME error here cus I can't just get the wt out of the dataframe
        wt = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)][['waitTime', 'directionId']].reset_index(drop = True)
        for i, waitdf in wt.iterrows():
            direction = waitdf['directionId']
            wait = waitdf['waitTime']
            RouteTimelines[route][direction][stationId].append(wait)
            if wait <= bunchThreshold:
                RouteBunchTimeline[route][direction][stationId] +=1


RouteTimelines = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
RouteBunchTimeline = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))

for route in df['routeId'].unique():
    for stop in df["stopSequence"].unique():
        #mean = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].mean()
        #FIXME error here cus I can't just get the wt out of the dataframe
        wt = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopSequence'] == stop)][['waitTime', 'directionId']].reset_index(drop = True)
        for i, waitdf in wt.iterrows():
            direction = waitdf['directionId']
            wait = waitdf['waitTime']
            RouteTimelines[route][direction][stop].append(wait)
            if wait <= bunchThreshold:
                RouteBunchTimeline[route][direction][stop] +=1

for i,stop in df.iterrows():
    if stop['waitTime'] != -1:
        if stop['waitTime'] <= bunchThreshold:
            RouteBunches[stop['routeId']] +=1
            StopBunches[stop['stopId']] +=1

rdf = DataFrame(columns=['Route', 'Direction', 'Station', 'MedianWait', 'Bunched Trains'])
for direction in [0,1]:
    for station in RouteTimelines[801][direction].keys():
        route = 801
        MedianWait = np.median(RouteTimelines[route][direction][station])
        bunches = RouteBunchTimeline[route][direction][station]
        row = {'Route': route, 'Direction': direction, 'Station': station, 'MedianWait': MedianWait, 'Bunched Trains': bunches}
        rdf = rdf._append(row, ignore_index = True)
'''
print(rdf.to_string())

print(RouteTimelines[801])


print(np.mean(RouteTimelines[801][80120]))
print(RouteBunchTimeline[801][80120])

print(rdf.to_string())
'''
#plot 801 route timeline
#ax = rdf.plot.bar(x='Station', y='MeanWait')
rdf = rdf.astype({'Route': 'int32', 'Direction': 'int32', 'Station': 'int32', 'Bunched Trains': 'int32'})
ax = rdf[rdf['Route'] == 801][['Station', 'MedianWait', 'Bunched Trains']].plot.bar(x='Station', rot=1)
ax = ax.tick_params('x', rotation=90)
plt.show()
plt.savefig('bunched_bars')
print(rdf.to_string())


'''
For each line go stop by stop and track wait times and bunching times
plot a few graphs
1. wait times over at each stop along the line
2. stations where bunching occured
3. 
'''