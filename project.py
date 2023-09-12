from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests
import json
import re
import sys

'''

# Project: Get the weather forecast for a given ZIP code
# Video Demo:  <URL HERE>
# Description: This program gets the weather forecast for a given ZIP code. 
The program uses the NWS API to get the forecast.

Input:
Input is in the form of a valid zip code. The user enters a ZIP code to get the forecast for. 
The zip code is validated using a regular expression and the user can enter 99999 to exit the program.
The input will loop until either a valid ZIP code is entered or the user enters 99999 to exit the program.

Output:
The program outputs the forecast for the ZIP code entered by the user. Included information is:
    The name of the location
    The temperature
    The chance of precipitation
    The wind speed and direction
    The forecast

Workflow:
Step 1: Get the ZIP code from the user

The program gets the ZIP code from the user and is validated using a regular expression. If the ZIP code is not valid, the program exits.
The program accepts '99999' as a valid ZIP code to exit the program.

Step 2: Get the latitude and longitude of the ZIP code

The program uses the Nominatim geocoder to get the latitude and longitude of the ZIP code and returns the latitude and longitude rounded to 4 decimal places.
The location is also returned.

Step 3: Get the NWS forecast URL for the ZIP code

This step is necessary to get the properly formatted URL for the NWS API. The program uses the latitude and longitude to get the URL.
This URL will then be used to get the forecast.

Step 4: Get the NWS forecast for the ZIP code

This step uses the URL returned in step 3 to get the forecast for the ZIP code. The program uses the requests library to make a GET request to the NWS API.
A JSON response is returned and parsed using the json library. The program then returns the forecast data.
Two forecast time periods are returned.

Step 5: Print the forecast

The program prints the forecast for the ZIP code. The program prints the following information:
    The name of the location
    The temperature
    The chance of precipitation
    The wind speed and direction
    The forecast

URL sources and Modules used:

The program uses the NWS API to get the forecast.
The program uses the geopy library to get the latitude and longitude of a ZIP code.
The program uses the Nominatim geocoder to get the latitude and longitude of a ZIP code.
The program uses the RateLimiter to avoid hitting rate limits.
The program uses the requests library to make HTTP requests.
The program uses the json library to parse JSON responses.
The program uses the re library to validate the ZIP code.

'''
def main():
    
    #Main function
    
    # Get the ZIP code from the user
    zip_code=get_user_input()
    
    # Get the latitude and longitude of the ZIP code
    long,lat,address=get_long_lat(zip_code)
            
    # Get the NWS forecast URL for the ZIP code
    url=get_nws_forecast_url(long,lat)
    
    # Get the NWS forecast for the ZIP code
    # Two forecasts are returned
    forecast1,forecast2=get_nws_forecast(url)
    
    # Print the forecast
    print_forecast(forecast1,address)
    print_forecast(forecast2)
    
    # Exit the program
    sys.exit()
    

def print_forecast(forecast1,address='skip'):
    
    # Print the forecast
    # Input: forecast (dictionary)
    
    if address!='skip':
        print(' ')     
        print(f"Forecast for {address}:")
    print(' ')
    print(f"{forecast1['name']}:")
    print(f"Temperature: {forecast1['temperature']} {forecast1['temperatureUnit']}")
    print(f"Chance of precipitation: {forecast1['probabilityOfPrecipitation']}%")
    print(f"Wind: {forecast1['windSpeed']} {forecast1['windDirection']}")
    print('Forecast:')   
    print(forecast1['shortForecast'])
    print(forecast1["detailedForecast"])
    
    
def get_user_input():
    # Get the ZIP code from the user
    # Input: None
    # Output: zip_code (string)
    
    # Loop until the user enters a valid ZIP code
    # Or enters 99999 to exit    
    while True:
        
        # Get the ZIP code from the user
        zip_code= str(input("Enter a zip code to get the forecast for (99999 to exit.): ").strip())
        
        # Check if the user wants to exit
        if zip_code=="99999":
            sys.exit("Exiting program.")
        
        # Check if the ZIP code is valid
        if not valid_zip(zip_code):
            sys.exit('Invalid zip code.')
    
        # Return the ZIP code
        return zip_code

def get_long_lat(zip_code):
    
    # Get the latitude and longitude of a ZIP code
    # Input: zip_code (string)
    try:
        # Use Nominatim to get the latitude and longitude of a ZIP code
        geolocator = Nominatim(user_agent="Getzipforweather")  # replace "geoapiExercises" with a custom user-agent name

        # Use RateLimiter to avoid hitting rate limits
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        
        # Get the location data
        location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
        
        # Get the latitude and longitude from the location data
        lat = location.latitude
        long = location.longitude
        
        #return the lat and long rounded to 4 decimal places
        
        return float(round(lat,4)), float(round(long,4)),location.address
    except (AttributeError):
        sys.exit("Can not find latitude and longitude for the given zip code.")
        
def get_nws_forecast_url(long,lat):
    
    # Get the NWS forecast URL for a given latitude and longitude
    # Input: long (float), lat (float)
    
    # Construct the URL for the NWS API
    url = f"https://api.weather.gov/points/{long},{lat}"

    # Make a GET request to NWS API
    resp = requests.get(url)

    # Parse the JSON response
    parsed_data = json.loads(resp.text)

    # Get the "forecast" URL from the "properties" and "forecast" object
    url = parsed_data["properties"]["forecast"]

    # Return the forecast URL
    
    return url

def get_nws_forecast(url):
    
    # Get the NWS forecast for a given URL
    # Input: url (string)
    # Output: forecast_data (dictionary)
    
    # Make a GET request to the NWS API
  
    try:
        # Make a GET request to NWS API
        resp = requests.get(url)
        forecast_data = resp.json()
        
        # Return the forecast data
        forecast_1=parse_nws_forecast(forecast_data,1)
        forecast_2=parse_nws_forecast(forecast_data,2)
        
        return(forecast_1,forecast_2)
    
    except :
        
        sys.exit("Zip code is not recognized by the NWS API.")

def parse_nws_forecast(data,number): 
    # Parse the NWS forecast data
    # Input: data (dictionary), number (int)
    # Output: weather_info (dictionary) 
    
    # Loop through the periods in the forecast data
     for period in data['properties']['periods']:
        if period['number'] == number:
            weather_info = {
                "name": period['name'],
                "temperature": period['temperature'],
                "temperatureUnit": period['temperatureUnit'],
                "probabilityOfPrecipitation": period['probabilityOfPrecipitation']['value'],
                "windSpeed": period['windSpeed'],
                "windDirection": period['windDirection'],
                "icon": period['icon'],
                "shortForecast": period['shortForecast'],
                "detailedForecast": period['detailedForecast']
            }
            return weather_info
    
def valid_zip(zip_code):
    
    # Check if a ZIP code is valid
    # Input: zip_code (string)
    
    # Use a regular expression to check if the ZIP code is valid
    pattern = r'^\d{5}(-\d{4})?$'
    
    # Return True if the ZIP code is valid, False otherwise
    if zip_code=='00000':
        return False
    else:
        return re.match(pattern, zip_code) is not None

if __name__ == "__main__":
    main()
    
