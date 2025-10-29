import requests
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict
from deepdiff import DeepDiff
import time

agencyKey = 'lametro' # also we have lametro-rail
endpoint = "https://api.goswift.ly" # mock is https://stoplight.io/mocks/swiftly-inc/realtime-standalone/28436057
with open('secrets.txt') as f:
    token = f.readline().strip('\n')



def getTripUpdates():
  resp = requests.get(endpoint+ f"/real-time/{agencyKey}/gtfs-rt-trip-updates?format=json", headers={"Authorization":token})
  # dumpJsonToFile(resp.text, "tripupdates.json", fromText=True)
  return json.loads(resp.text)




def getRouteStarts(routes):
  data = dict(getTripUpdates())
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

def getRouteUpdates(routes, prev):
  data = dict(getTripUpdates())
  updates = defaultdict(list) 
  for entry in data["entity"]:
    routeID = str(entry['tripUpdate']['trip']['routeId'])
    routeID = routeID[0:routeID.find('-')]
    if routeID in routes:
      updates[routeID].append(entry['tripUpdate'])
      #if(updates['scheduleRelationship'] == 'SCHEDULED'):
        #if(updates['stopTimeUpdate']):
          #dt_object = datetime.fromtimestamp(int([0]['arrival']['time']))

  return [updates, DeepDiff(prev, updates, ignore_order=True)]

routes = ['207', '754']

#TODO actually save the files to json or whatever we need
def diffUpdates(routes, interval = 5):
  start = getRouteStarts(routes)
  #save start to json
  while(True):
    updates = getRouteUpdates(routes, start)
    if updates[1] != {}:
      print("update found")
      start = updates[0]
      #save updates[1] for the diff, updates[0] for the raw data
    else:
      print("Nothing found")
    time.sleep(interval)