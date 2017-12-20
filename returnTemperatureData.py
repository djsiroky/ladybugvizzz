from getWeatherData import returnWeatherDataDict
import ladybug
import sys
from ladybug.analysisperiod import AnalysisPeriod
import googlemaps
import json
import pandas as pd

def f(x):
    x = x * 1.8 + 32
    return float(x)

def lambda_handler(loc):
    ap = AnalysisPeriod()
    
    gmaps = googlemaps.Client(key='AIzaSyC7ZVjH0QZbR3T96_GO25dcP-woiA4hrvI')
    # Geocode my hardcoded address
    geocode_result = gmaps.geocode(loc)
    addr = geocode_result[0]["formatted_address"]
    loc = geocode_result[0]["geometry"]["location"]
    
    wdd = returnWeatherDataDict(longitude=loc["lng"], latitude=loc["lat"])
    
    df = pd.DataFrame({'row': wdd["dryBulbTemperature"]})
    df['row'] = df['row'].astype('str') 
    
    data = pd.DataFrame(df.row.str.split(' at ',1).tolist(),
                                       columns = ['temp','dt'])
    
    data['dt'] = pd.to_datetime(data['dt'], format="%d %b %H:%M")
    data['temp'] = data['temp'].astype('float64')
    data['temp'] = data['temp'].apply(f)
    #json_filename = sys.argv[2] + '.json'
    #csv_filename = sys.argv[2] + '.csv'
    j = data.to_json(orient='records')
    r = dict(place=addr, data=j)
    #data.to_csv(path_or_buf=csv_filename)
    return r
