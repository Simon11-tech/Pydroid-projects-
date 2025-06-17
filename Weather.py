import requests

API_KEY = "3b913d42cccd635b95e2c99cf48b326c"
city = input("Enter city name:New York")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print(f"\nWeather in {city.title()}:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Condition: {data['weather'][0]['description'].title()}")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind: {data['wind']['speed']} m/s")
else:
    print("❌ Error:", data.get("message", "Unknown error"))