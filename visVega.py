from getWeatherData import returnWeatherDataDict
import ladybug
from ladybug.analysisperiod import AnalysisPeriod
import googlemaps
import json
import pandas as pd
from altair import Row, Column, Chart, Text, Color, Scale

ap = AnalysisPeriod()

gmaps = googlemaps.Client(key='AIzaSyC7ZVjH0QZbR3T96_GO25dcP-woiA4hrvI')

# Geocode my hardcoded address
geocode_result = gmaps.geocode('2460 Pershing Road, Kansas City, MO 64108')
loc = geocode_result[0]["geometry"]["location"]

wdd = returnWeatherDataDict(longitude=loc["lng"], latitude=loc["lat"])

df = pd.DataFrame({'row': wdd["dryBulbTemperature"]})
df['row'] = df['row'].astype('str') 

#print(df["row"].str.split(' at ', 1).tolist())
data = pd.DataFrame(df.row.str.split(' at ',1).tolist(),
                                   columns = ['temp','dt'])

data['dt'] = pd.to_datetime(data['dt'], format="%d %b %H:%M")
data['temp'] = data['temp'].astype('float64')
chart = Chart(data).mark_text(
               applyColorToBackground=True,
           ).encode(
               row=Row('dt:T', timeUnit='hours'),
               column=Column('dt:T', timeUnit='month'),
               text='temp',
               color=Color('temp',
                    scale=Scale(range='blueorange')
                )
           ).configure_scale(
               textBandWidth=30,
               bandSize=15
           )
           
chart.max_rows = 8761
chart.savechart('plot.html')
