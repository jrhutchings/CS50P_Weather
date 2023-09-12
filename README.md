# Project: Get the weather forecast for a given ZIP code
# Video Demo:  https://youtu.be/ZckiQG9NoTI
# Description: This program gets the weather forecast for a given ZIP code. 
               

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

NWS API to get the forecast.
geopy library to get the latitude and longitude of a ZIP code.
Nominatim geocoder to get the latitude and longitude of a ZIP code.
RateLimiter to avoid hitting rate limits.
requests library to make HTTP requests.
json library to parse JSON responses.
re library to validate the ZIP code.

Functions:

1. get_zip_code()
   This function prompts the user to enter a ZIP code and validates the input using a regular expression. I
2. get_location_info(zip_code)
   This function uses the geopy library to get the latitude and longitude of a ZIP code. T
3. get_forecast_url(latitude, longitude)
   This function constructs the URL for the NWS API using the latitude and longitude of the ZIP code. 
4. get_forecast_data(url)
   This function uses the requests library to make a GET request to the NWS API and get the forecast data for the ZIP code.
5. parse_forecast_data(forecast_data)
   This function parses the forecast data returned by the NWS API and extracts the relevant information. 
6. print_forecast(forecast, location)
   This function prints the forecast information for the ZIP code. 
7. main()
   This function is the main entry point of the program. 
