import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


bunchThreshold = 5.0

file = 'station_data_4.csv'
df = pd.read_csv(file, index_col=0)
df.drop_duplicates(subset=['vehicleId', 'stopId', 'directionId'])


RouteBunches = defaultdict(int)
StopBunches = defaultdict(int)
RouteTimelines = defaultdict(lambda : defaultdict(list))
RouteBunchTimeline = defaultdict(lambda : defaultdict(int))
#{routeId: {stopId: [waitTime/bunchNumber]}


for route in df['routeId'].unique():
    for stationId in df["stopId"].unique():
        #mean = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].mean()
        #FIXME error here cus I can't just get the wt out of the dataframe
        wt = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].reset_index(drop = True)
        for i, wait in enumerate(wt):
            RouteTimelines[route][stationId].append(wait)
            if wait <= bunchThreshold:
                RouteBunchTimeline[route][stationId] +=1


for i,stop in df.iterrows():
    if stop['waitTime'] != -1:
        if stop['waitTime'] <= bunchThreshold:
            RouteBunches[stop['routeId']] +=1
            StopBunches[stop['stopId']] +=1

rdf = DataFrame(columns=['Route', 'Station', 'MeanWait', 'Bunched Trains'])
for station in RouteTimelines[801].keys():
    route = 801
    MeanWait = np.mean(RouteTimelines[route][station])
    bunches = RouteBunchTimeline[route][station]
    row = {'Route': route, 'Station': station, 'MeanWait': MeanWait, 'Bunched Trains': bunches}
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
ax = rdf.plot.bar(rot=1)
plt.show()


'''
For each line go stop by stop and track wait times and bunching times
plot a few graphs
1. wait times over at each stop along the line
2. stations where bunching occured
3. 
'''