from getWeatherData import returnWeatherDataDict
import ladybug
import sys
from ladybug.analysisperiod import AnalysisPeriod
import googlemaps
import json
import pandas as pd
from altair import Row, Column, Chart, Text, Color, Scale, Bin, Axis, Legend

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
json_filename = sys.argv[2] + '.json'
data.to_json(path_or_buf=json_filename)

colors =   ["#67001f",
            "#b2182b",
            "#d6604d",
            "#f4a582",
            "#fddbc7",
            "#d1e5f0",
            "#92c5de",
            "#4393c3",
            "#2166ac",
            "#053061"]

colors = colors[::-1]

#d = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108]
d = [0, 120]
r = Row('dt:T', timeUnit='hours', axis=Axis(title='Hour of day'))
c = Column('dt:T', 
           timeUnit='monthdate', 
           axis=Axis(format=u'%b', labels=False, title='Month')
        ) 
col = Color('temp:N',
            bin=Bin(step=12),
            scale=Scale(domain=[0,120], range=colors, clamp=True, zero=True),
            #scale=Scale(range=colors, domain=[0, 120], zero=True),
            legend=Legend(title="Temperature", format=u'.0f')
           )

chart = Chart(data).mark_text(
                applyColorToBackground=True
            ).encode(
               row=r,
               column=c,
               text=Text('blanks'),
               color=col
           ).configure_scale(
               textBandWidth=3,
               bandSize=25
           )
           
chart.max_rows = 8761
filename = sys.argv[2] + ".html"
chart.savechart(filename)
