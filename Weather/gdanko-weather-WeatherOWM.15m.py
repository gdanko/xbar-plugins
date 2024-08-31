#!/usr/bin/env python3

# <xbar.title>Weather OpenWeatherMap</xbar.title>
# <xbar.version>v0.1.0</xbar.version>
# <xbar.author>Gary Danko</xbar.author>
# <xbar.author.github>gdanko</xbar.author.github>
# <xbar.desc>This plugin displays the weather using openweathermap.org]</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/gdanko/xbar-plugins/blob/main/Weather/gdanko-weather-WeatherOWM.15m.py</xbar.abouturl>
# <xbar.var>string(VAR_WEATHER_OWM_LOCATION="San Diego, CA, US"): The location to use</xbar.var>
# <xbar.var>string(VAR_WEATHER_OWM_API_KEY=""): The OpenWeatherMap API key</xbar.var>
# <xbar.var>string(VAR_WEATHER_OWM_UNITS="F"): The unit to use: (C)elsius, (F)ahrenheit, or (K)elvin</xbar.var>

import json
import os

def pad_float(number):
    return '{:.2f}'.format(float(number))

def get_defaults():
    location = os.getenv('VAR_WEATHER_OWM_LOCATION', 'San Diego, CA, US')
    api_key = os.getenv('VAR_WEATHER_OWM_API_KEY', '')
    valid_units = ['C', 'F', 'K']
    units = os.getenv('VAR_WEATHER_OWM_UNITS', 'F')
    if not units in valid_units:
        units = 'F'
    
    return location, api_key, units

def main():
    try:
        import requests

        location, api_key, units = get_defaults()

        units_map = {
            'C': 'metric',
            'F': 'imperial',
            'K': '',
        }

        if api_key == '':
            print('Failed to fetch the weather')
            print('---')
            print('Missing API key')
        else:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units_map[units]}'
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    weather_data = json.loads(response.content)
                    print(f'{location} {pad_float(weather_data["main"]["temp"])}°{units}')
                except:
                    print('Failed to fetch the weather')
                    print('---')
                    print('Failed to parse the JSON data')
            else:
                print('Failed to fetch the weather')
                print('---')
                print(f'Non-200 status code: {response.status_code}')

    except ModuleNotFoundError:
        print('Error: missing "requests" library.')
        print('---')
        import sys
        import subprocess
        subprocess.run('pbcopy', universal_newlines=True,
                       input=f'{sys.executable} -m pip install requests')
        print('Fix copied to clipboard. Paste on terminal and run.')

if __name__ == '__main__':
    main()