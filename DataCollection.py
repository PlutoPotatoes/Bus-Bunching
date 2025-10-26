import requests
import json
import pandas as pd

agencyKey = 'lametro' # also we have lametro-rail
endpoint = "https://api.goswift.ly" # mock is https://stoplight.io/mocks/swiftly-inc/realtime-standalone/28436057
token = "9c91bdbe6aaea1446ca2343721cb49cc" # format is "Authorization: token"