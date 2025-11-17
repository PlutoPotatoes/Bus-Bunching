import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
from collections import defaultdict


bunchThreshold = 5.0

file = 'station_data.csv'
df = pd.read_csv(file, index_col=0)

RouteBunches = defaultdict(int)
StopBunches = defaultdict(int)


df = df[df['routeId'] == 801]
for stationId in df["stopId"].unique():
    mean = df[(df['waitTime'] != -1) & (df['stopId'] == stationId)]['waitTime'].mean()
    print(f"{stationId} mean: {mean}")


for i,stop in df.iterrows():
    if stop['waitTime'] != -1:
        if stop['waitTime'] <= bunchThreshold:
            RouteBunches[stop['routeId']] +=1
            StopBunches[stop['stopId']] +=1

print(RouteBunches)
print(StopBunches)