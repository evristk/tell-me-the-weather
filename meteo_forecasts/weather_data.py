import meteo_forecasts.constants as constants


class WeatherPredictionData:
    def __init__(self):
        self.predictions = {}

    def get_data(self, key):
        return self.predictions[key]

    def set_data(self, key, value):
        self.predictions[key] = value

    def set_correct_time(self, time):
        self.predictions[constants.TIME_KEY] = time

    def __str__(self):
        return "%s | %s | %s" % (self.predictions[constants.TIME_KEY],
                                 self.predictions[constants.TEMPERATURE_KEY],
                                 self.predictions[constants.WEATHER_KEY])


class WeatherEntry:
    def __init__(self, datetime, weather_data):
        self.datetime = datetime
        self.weather_data = weather_data

    def get_datetime(self):
        return self.datetime

    def get_weather_data(self):
        return self.weather_data
