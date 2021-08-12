import requests


params = {
    'q': 'Tashkent',
    'appid': 'd316f85b72aa7669c75a4ea3238150c9',
}

response = requests.get('https://api.openweathermap.org/data/2.5/weather', params)
response_json = response.json()
print(response_json)

# with open('data.json', mode='w')as file:
#     json.dump(response_json, file, indent=4)
