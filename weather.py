import requests
import json
from prettytable import PrettyTable
from datetime import datetime
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/"
CITY = "New York"  # Default city; user can change this in the code or as an input.
def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        main = data['main']
        wind = data['wind']
        weather_desc = data['weather'][0]['description']
        
        # Parse weather data
        current_weather = {
            "City": city,
            "Temperature": main["temp"],
            "Humidity": main["humidity"],
            "Pressure": main["pressure"],
            "Wind Speed": wind["speed"],
            "Description": weather_desc,
            "Time": datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return current_weather
    else:
        print("Error:", response.status_code)
        return None
      def get_weather_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        forecast_list = []
        for item in data['list']:
            forecast = {
                "Date": datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                "Temperature": item['main']['temp'],
                "Weather": item['weather'][0]['description'],
                "Humidity": item['main']['humidity'],
                "Wind Speed": item['wind']['speed']
            }
            forecast_list.append(forecast)
        
        return forecast_list
    else:
        print("Error:", response.status_code)
        return None
def display_current_weather(weather_data):
    if weather_data:
        table = PrettyTable()
        table.field_names = ["Parameter", "Value"]
        for key, value in weather_data.items():
            table.add_row([key, value])
        print("Current Weather:")
        print(table)
    else:
        print("No data to display.")
def display_forecast(forecast_data):
    if forecast_data:
        print("\n5-Day Weather Forecast:")
        table = PrettyTable()
        table.field_names = ["Date", "Temp (°C)", "Weather", "Humidity (%)", "Wind Speed (m/s)"]
        
        for item in forecast_data:
            table.add_row([item["Date"], item["Temperature"], item["Weather"], item["Humidity"], item["Wind Speed"]])
        
        print(table)
    else:
        print("No forecast data to display.")
def save_data_to_file(data, filename="data/weather_data.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
def main():
    city = input("Enter the city name: ")
    
    # Fetch and display current weather
    current_weather = get_current_weather(city)
    display_current_weather(current_weather)
    
    # Fetch and display forecast
    forecast_data = get_weather_forecast(city)
    display_forecast(forecast_data)
    
    # Optionally, save data to a file
    save_data = input("Do you want to save this data to a file? (yes/no): ")
    if save_data.lower() == 'yes':
        save_data_to_file({"current_weather": current_weather, "forecast": forecast_data})
        print("Data saved successfully.")

