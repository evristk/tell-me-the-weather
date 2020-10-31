import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

index = requests.get("https://www.meteo.gr/index-en.cfm")
index = BeautifulSoup(index.text, 'lxml')
cities = index.find_all('a', {'href' : re.compile('city_id=')})

city_to_id = {}
for city in cities:
    city_name = city.get_text().strip()
    city_id = re.search(r'\d+', str(city)).group()

    city_to_id[city_name] = city_id

df = pd.DataFrame(city_to_id.items(), columns=['city_name', 'city_id'])
df.to_csv('meteogr_city_to_id.csv')

