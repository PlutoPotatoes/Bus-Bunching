import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
from collections import defaultdict
import matplotlib as plt


bunchThreshold = 5.0

file = 'station_data_4.csv'
df = pd.read_csv(file, index_col=0)
df.drop_duplicates(subset=['vehicleId', 'stopId', 'directionId'])


RouteBunches = defaultdict(int)
StopBunches = defaultdict(int)


for route in df['routeId'].unique():
    for stationId in df["stopId"].unique():
        mean = df[(df['routeId'] == route) & (df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].mean()
        print(f"{stationId} mean: {mean}")


    for i,stop in df.iterrows():
        if stop['waitTime'] != -1:
            if stop['waitTime'] <= bunchThreshold:
                RouteBunches[stop['routeId']] +=1
                StopBunches[stop['stopId']] +=1

print(RouteBunches)
print(StopBunches)

'''
For each line go stop by stop and track wait times and bunching times
plot a few graphs
1. wait times over at each stop along the line
2. stations where bunching occured
3. 
'''