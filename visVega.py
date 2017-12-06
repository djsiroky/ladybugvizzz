from getWeatherData import returnWeatherDataDict
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyC7ZVjH0QZbR3T96_GO25dcP-woiA4hrvI')

# Geocode my hardcoded address
geocode_result = gmaps.geocode('2460 Pershing Road, Kansas City, MO 64108')
print(geocode_result)

# returnWeatherDataDict("")