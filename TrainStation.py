import json
import pandas as pd
from pandas import DataFrame


with open('media\initial_data_20251111_030908.json', 'r') as f:
    df = DataFrame(dict(json.load(f)))

print(df.to_string())
TrainStations = {}

