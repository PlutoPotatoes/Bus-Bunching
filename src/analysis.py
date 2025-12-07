import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from metroutils import routeIDtoName

bunchThreshold = 7
#11-19 - 11-30 train data
file = 'media/combined_station_data.csv'


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
    for stop in df[df['routeId'] == route]["stopSequence"].unique():
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

print(RouteBunches)
routes = [801]
for route in routes:

    rdf = DataFrame(columns=['Route', 'Direction', 'Station', 'MedianWait', 'Bunch Percentage'])
    for direction in [0,1]:
        for station in RouteTimelines[route][direction].keys():
            MedianWait = np.mean(RouteTimelines[route][direction][station])
            PercentBunched = RouteBunchTimeline[route][direction][station]/len(RouteTimelines[route][direction][station])
            bunches = RouteBunchTimeline[route][direction][station]
            row = {'Route': route, 'Direction': direction, 'Station': station, 'Median Wait': MedianWait, 'Bunched Trains': bunches, 'Bunch Percentage': PercentBunched}
            rdf = rdf._append(row, ignore_index = True)

    #plot 801 route timeline
    #ax = rdf.plot.bar(x='Station', y='MeanWait')
    rdf = rdf.astype({'Route': 'int32', 'Direction': 'int32', 'Station': 'int32', 'Bunched Trains': 'int32', 'Bunch Percentage' : 'float16'})
    #ax = rdf[rdf['Route'] == route][['Station', 'MedianWait', 'Bunch Percentage']].plot.bar(x='Station', rot=1)
    #ax = ax.tick_params('x', rotation=90)
    #plt.show()
    #plt.savefig('Bunched_bars')

    rdf = rdf.dropna(axis=0, subset=['Median Wait'])
    rdf = rdf[rdf['Direction'] == 0]
    model = LinearRegression()
    x = rdf[['Bunch Percentage']]
    y = rdf['Median Wait']
    model.fit(x,y)
    r = model.score(x,y)

    y_pred = model.predict(x)
    plt.scatter(x, y, color='orange', label='Observed')
    plt.plot(x, y_pred, color='red', label='Prediction')
    plt.xlabel('Stop Number on Line')
    plt.ylabel('Bunch Percentage at Station')
    plt.title(f"E Line Stop Order and Bunch Rate Regression")
    plt.legend()
    plt.show()
    print(f"Median Wait for {route} = {np.median(rdf['MedianWait'])}")
    print(f"R2 Score for {route} = {r}")

'''
bunched data includes all trains, unbunched does not count bunched trains in the total

801 bunched = 13.6
801 bunched 7.5 = 15.35
801 unbunched = 12.5

802 bunched = 13.7
802 bunched 7.5 = 13.8
802 unbunched = 13.7

803 bunched = 14.6
803 bunched 7.5 = 14.6
803 unbunched = 14.6

804 bunched = 12.0
804 bunched 7.5 = 14.0
804 unbunched = 11.5

805 bunched = 16.85
805 bunched 7.5 = 16.9
805 unbunched = 16.85

807 bunched = 15.7
807 bunched 7.5 = 15.7
807 unbunched = 15.7


801 = A Line
802 = B line
803 = C line
804 = E Line
805 = D Line
807 = K line


R2 Scores for bunch percent and wait time:
801:0.176
802:0.085
803:0.00001
804:0.35
805:0.058
807:n/a
^Similar results when using total observed bunches
R2 Scores for station number and wait time were also horrible


R2 for Station predicting Bunch Percentage Direction 1
801:0.73
802:0.38
804:0.57/0.83

R2 for Station predicting Bunch Percentage Direction 0
801:0.78
802:0.57
804:0.48/0.84






'''