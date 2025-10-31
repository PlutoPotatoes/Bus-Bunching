import requests
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict
import jsonpatch
import time
from copy import deepcopy

agencyKey = 'lametro' # also we have lametro-rail
endpoint = "https://api.goswift.ly" # mock is https://stoplight.io/mocks/swiftly-inc/realtime-standalone/28436057
routes = ['207', '754']

with open('secrets.txt') as f:
    token = f.readline().strip('\n')

def getAPIData():
    # added checks and retries, in case connection fails, etc
    sleeptime = 1
    while True:
        try:
            resp = requests.get(endpoint+ f"/real-time/{agencyKey}/gtfs-rt-trip-updates?format=json", headers={"Authorization":token})
            if resp.status_code == 200:
                try:
                    jsondata = json.loads(resp.text)
                    return jsondata
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}. Retrying in {sleeptime} seconds...")
                    time.sleep(sleeptime)
                    sleeptime = min(sleeptime * 2, 60)
            else:
                print(f"Error: Received status code {resp.status_code}. Retrying in {sleeptime} seconds...")
                time.sleep(sleeptime)
                sleeptime = min(sleeptime * 2, 60)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying in {sleeptime} seconds...")
            time.sleep(sleeptime)
            sleeptime = min(sleeptime * 2, 60)

def getRoutes(routes):
    data = dict(getAPIData())
    updates = defaultdict(list) 
    for entry in data["entity"]:
        routeID = str(entry['tripUpdate']['trip']['routeId'])
        routeID = routeID[0:routeID.find('-')]
        if routeID in routes:
            updates[routeID].append(entry['tripUpdate'])
            #if(updates['scheduleRelationship'] == 'SCHEDULED'):
                #if(updates['stopTimeUpdate']):
                    #dt_object = datetime.fromtimestamp(int([0]['arrival']['time']))
    return updates

def collectionLoop(routes, interval = 5):
    start = getRoutes(routes) # initial data
    lastdata = deepcopy(start) # this is updated every loop
    diffs = [] # list of (timestamp, diff) tuples
    with open('initial_data.json', 'w') as f:
        json.dump(start, f, indent=4)
    with open('diffs.json', 'w') as f:
        while(True):
            time.sleep(interval)
            current = getRoutes(routes)
            diff = jsonpatch.make_patch(lastdata, current).to_string()
            if diff:
                timestamp = time.time()
                diffs.append(str(timestamp) + "\t" + diff)
                print(f"Change detected at {datetime.fromtimestamp(timestamp)}:")
                print(diff)
                with open('diffs.txt', 'a') as f:
                    f.write(str(timestamp) + "\t" + diff + "\n")
                lastdata = deepcopy(current)
        
collectionLoop(routes, interval=30)