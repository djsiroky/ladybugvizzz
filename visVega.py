from getWeatherData import returnWeatherDataDict
import ladybug
import sys
from ladybug.analysisperiod import AnalysisPeriod
import googlemaps
import json
import pandas as pd
from altair import Row, Column, Chart, Text, Color, Scale, Bin, Axis

def f(x):
    x = x * 1.8 + 32
    return float(x)

ap = AnalysisPeriod()

gmaps = googlemaps.Client(key='AIzaSyC7ZVjH0QZbR3T96_GO25dcP-woiA4hrvI')

# Geocode my hardcoded address
geocode_result = gmaps.geocode(sys.argv[1])
loc = geocode_result[0]["geometry"]["location"]

wdd = returnWeatherDataDict(longitude=loc["lng"], latitude=loc["lat"])

df = pd.DataFrame({'row': wdd["dryBulbTemperature"]})
df['row'] = df['row'].astype('str') 

#print(df["row"].str.split(' at ', 1).tolist())
data = pd.DataFrame(df.row.str.split(' at ',1).tolist(),
                                   columns = ['temp','dt'])
data['blanks'] = ""

data['dt'] = pd.to_datetime(data['dt'], format="%d %b %H:%M")
data['temp'] = data['temp'].astype('float64')
data['temp'] = data['temp'].apply(f)

colors = ["#67001f","#b2182b","#d6604d","#f4a582","#fddbc7","#d1e5f0","#92c5de","#4393c3","#2166ac","#053061"]
colors = colors[::-1]
chart = Chart(data).mark_text(
               applyColorToBackground=True,
           ).encode(
               row=Row('dt:T', timeUnit='hours', axis=Axis(title='Hour of day')),
               column=Column('dt:T', timeUnit='monthdate', axis=Axis(
            format=u'%b', labels=False, title='Month'
)),
               text=Text('blanks'),
               color=Color('temp:N', bin=Bin(maxbins=10, step=5), clamp=True,
                    scale=Scale(range=colors, domain=[0, 100]), axis=Axis(title='Temperature')
                )
           ).configure_scale(
               textBandWidth=2,
               bandSize=15
           )
           
chart.max_rows = 8761
chart.savechart('plot.html')
