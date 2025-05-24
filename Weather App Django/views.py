def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    try:
        # Fetch current weather data
        response = requests.get(current_weather_url.format(city, api_key)).json()

        # Check if 'coord' key exists in response
        if 'coord' not in response:
            print(f"Error: 'coord' key not found in the response for city: {city}")
            return None, []

        lat, lon = response['coord']['lat'], response['coord']['lon']

        # Fetch forecast data
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

        # Check if 'daily' key exists in forecast response
        if 'daily' not in forecast_response:
            print(f"Error: 'daily' key not found in the forecast response for city: {city}")
            return None, []

        # Process weather data
        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        # Process daily forecasts
        daily_forecasts = []
        for daily_data in forecast_response['daily'][:5]:
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
            })

        return weather_data, daily_forecasts

    except requests.exceptions.RequestException as e:
        print(f"RequestException occurred: {e}")
        return None, []

    except KeyError as e:
        print(f"KeyError occurred: {e}")
        return None, []
