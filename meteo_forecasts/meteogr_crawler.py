from bs4 import BeautifulSoup
import requests as req
import re
import meteo_forecasts.constants as constants
import meteo_forecasts.weather_data as weather_data
import datetime


meteo_url = 'https://www.meteo.gr/cf-en.cfm?city_id=23'


def get_html_data(url=meteo_url):
    r = req.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_date_weather_tags(soup):
    # Find div with id='Prognoseis'. This contains the table with the predictions
    predictions = soup.find(id='prognoseis')
    return predictions.find_all(re.compile('td|tr'), {'class': re.compile('forecastDate|perhour')})


def extract_weather_entry(tag):
    # Extract data from element tag
    tds = tag.findChildren('td', recursive=False)
    hour = trim(tag.find('td', {'class': 'fulltime'}).get_text())
    dt_time = datetime.datetime.strptime(hour, "%H:%M")
    # H = dt_time.hour
    # M = dt_time.minute
    temperature = trim(tag.find('td', {'class': 'temperature'}).get_text())
    weather = trim(tag.find('td', {'class': 'phenomeno-name'}).get_text())
    # Create object
    w_data = weather_data.WeatherPredictionData()
    w_data.set_data(constants.TIME_KEY, dt_time)
    w_data.set_data(constants.TEMPERATURE_KEY, temperature)
    w_data.set_data(constants.WEATHER_KEY, weather)
    return weather_data.WeatherEntry(dt_time, w_data)


def extract_date_info(tag):
    day_month = trim(tag.get_text().split(' ')[1])
    dd = re.search(r'\d+', day_month).group()
    month = re.search(r'[a-zA-Z]+', day_month).group()
    mm = datetime.datetime.strptime(month, '%B').month
    weather_dt = datetime.datetime(datetime.datetime.now().year, mm, int(dd)).date()
    return weather_dt


def get_datetime(correct_date, correct_time):
    return datetime.datetime(correct_date.year,
                       correct_date.month,
                       correct_date.day,
                       correct_time.hour,
                       correct_time.minute)

def trim(text):
    return text.replace('\n', ' ').strip()




