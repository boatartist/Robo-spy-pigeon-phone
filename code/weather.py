import requests, json

api_key = '82618e79d7798ce588410720817292fe'
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city_name='sydney'):
    url = f'{base_url}appid={api_key}&q={city_name}'
    print(url)
    response = requests.get(url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        temperature = round(float(y["temp"])-273.15, 2)
        z = x["weather"]
        description = z[0]["description"]
        icon_code = z[0]['icon']
        icon_url = f'https://openweathermap.org/img/wn/{icon_code}@2x.png'
        print(icon_url)
        icon = requests.get(icon_url).content
        with open('current_weather.png', 'wb') as f:
            f.write(icon)
        return temperature, description
    else:
        return None
    
get_weather()