# Author: Samuel Castro
# 11/19/2022
# The purpose of this assignment is to ask the user for their city or zip code preference, and then we request
# the weather forecast data from OpenWeatherMap and show the reader the data in a readable format.


import sys
import requests
import json


# The start of this program is to get the City and State requirements
# Making sure that a blank response is not allowed, and to determine the unit of temperature
def getCityInfo():
    cityName = input("Enter city name:  ")
    while cityName is None or len(str(cityName)) == 0:
        print('Please enter a city name!\nNo blank Responses allowed!')
        cityName = input("Enter city name:  ")
    stateAbb = input('Enter State abbreviation:Example is "CA"" for California ')
    while stateAbb is None or len(str(stateAbb)) == 0:
        print('Please enter a state abbreviation!\nNo blank Responses allowed!')
        stateAbb = input('Enter State abbreviation: ')
    units = input(
        "Connection is a go!\nEnter what type of temperature you would like:\n'F' for Fahrenheit\n'C' for Celsius\n'K' for Kelvin'\nEnter response here: ")
    if units.upper() not in ('F', 'C', 'K'):
        print("'F' for Fahrenheit\n'C' for Celsius\n'K' for Kelvin\nI am BOB\nand I will not tolerate bad responses!")
    return cityName, stateAbb, units


# This code is to get the users Zip Code input.
# I made sure to handle blank inputs and inputs that were too large and small
# This code also has a hadnle to determine what unit of measure the user would like.
def getZipCode():
    zipCode = input('Enter enter a *5* digit Zip Code:  ')
    while zipCode.isnumeric() and len(zipCode) != 5:
        print("BOB NEEDS A ZIPCODE WITH EXACTLY 5 NUMBERS!")
        zipCode = input('Enter enter a *5* digit Zip Code:  ')
    while zipCode is None or len(str(zipCode)) == 0:
        print('Stop messing with me!\nPlease input numbers for zipcode!')
        zipCode = input('Enter enter a *5* digit Zip Code:  ')
    units = input(
        "Connection is a go!\nEnter what type of temperature you would like:\n'F' for Fahrenheit\n'C' for Celsius\n'K' for Kelvin'\nEnter response here: ")
    while units.upper() is None or len(str(units)) == 0:
        print('I am BOB\nI will not tolerate blank responses!')
        units = input(
            "Please ReEnter what type of temperature you would like:\n'F' for Fahrenheit\n'C' for Celsius\n'K' for Kelvin'\nEnter response here: ")
    return zipCode, units


# This function creates the City URL.
# If the user chooses to input the city and state then they will go through the getCityInfor first and the inputs of city and state
# will be used in this specific block.
def createCityUrl(city, state):
    limit = 1
    url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&limit={limit}&appid=a046f34843d6a02960be2cf57497e95a'
    output = requests.request('GET', url1)
    if output.status_code == 200:
        output_json = output.json()
        latitude = output_json[0]['lat']
        longitude = output_json[0]['lon']
        return latitude, longitude
    else:
        print('Error. Please try submitting your responses again!')
        main()


# This function creates the Zipcode URL.
# If the user chooses to input a Zipcode then they will go through the getZipCode function first and the zipcode input they give
# will be used in this specific block.
def createZipUrl(zipCode):
    url2 = f'http://api.openweathermap.org/geo/1.0/zip?zip={zipCode}&appid=a046f34843d6a02960be2cf57497e95a'
    output = requests.request("GET", url2)
    if output.status_code == 200:
        output_json = output.json()
        latitude = output_json['lat']
        longitude = output_json['lon']
        return latitude, longitude
    else:
        print('Error. Please try submitting your responses again!')
        main()


# This function grabs the actual weather data using the api key and the latitude and longitude that was pulled from the
# previous requests. This block also determines which units of measure are used by using the methods below.
def getWeather(lat, lon, units):
    global output
    if units.upper() == "F":
        units = 'imperial'
    elif units.upper() == "C":
        units = 'metric'
    elif units.upper() == "K":
        units = 'kelvin'
    weather = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=a046f34843d6a02960be2cf57497e95a&units={units}'
    try:
        output = requests.request("GET", weather)
        output.raise_for_status()
        output = output.json()
    except requests.exceptions.HTTPError as error:
        print(f'HTTP error... {error}')
        main()
    print('*' * 30)
    print(f"Current weather conditions for:\nCity: {output['name']}\nCountry: {output['sys']['country']}")
    print(f"Description : {output['weather'][0]['description']}")
    print(f"Current Temp: {output['main']['temp']}\u00b0")
    print(f"Feels like  : {output['main']['feels_like']}\u00b0")
    print(f"High Temp   : {output['main']['temp_max']}\u00b0")
    print(f"Low Temp    : {output['main']['temp_min']}\u00b0")
    print('*' * 30)

# Main loop that introduces the program and grants the user the ability to input a city name or a zipcode.
# This loop goes through all the function before to finally go to the get_weather function where the actual weather data is pulled
def main():
    while True:
        print('=' * 30)
        print("HELLO! I am BOB, your personal weatherman for the city of your choice!")
        print('=' * 30)
        userInput = str(input(
            "Please enter\n'1' for city name\n'2' for 5 digit zipcode\n'3' to end my program, aka my life:  "))
        if userInput == '1':
            city_name, state_name, units = getCityInfo()
            latitude, longitude = createCityUrl(city_name, state_name)
            getWeather(latitude, longitude, units)
            main()
        elif userInput == '2':
            zipCode, units = getZipCode()
            latitude, longitude = createZipUrl(zipCode)
            getWeather(latitude, longitude, units)
            main()
        elif userInput.lower() == '3':
            print('Thank you using my program!\nYou have fufilled my life purpose!\nBye bye!')
            sys.exit()
        while userInput is None or len(str(userInput)) == 0:
            print('Please enter a response bruh.')
            main()


if __name__ == '__main__':
    # call main function
    main()
