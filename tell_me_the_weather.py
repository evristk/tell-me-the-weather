import datetime as dt
from meteo_forecasts import meteogr_crawler as mc
import argparse
import importlib

module_name = 'meteo_forecasts'
importlib.import_module(module_name)


def get_forecasts():
    soup = mc.get_html_data()
    rows = mc.get_date_weather_tags(soup)
    predictions = {}
    date = ''

    for row in rows:
        if 'perhour' in row['class']:
            # Forecast
            weather_entry = mc.extract_weather_entry(row)
            time = weather_entry.get_datetime()
            weather = weather_entry.get_weather_data()
            # Fix datetime
            weather.set_correct_time(mc.get_datetime(date, time))
            predictions[date].append(weather)
        elif 'forecastDate' in row['class']:
            # Date
            date = mc.extract_date_info(row)
            predictions[date] = []
    return predictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-afterDays',
                        type=int,
                        choices=[1, 2, 3],
                        help='After how many days will the forecast be?',
                        required=False,
                        default=1)
    args = parser.parse_args()
    after_days = args.afterDays

    today = dt.date.today()
    tomorrow = today + dt.timedelta(days=after_days)
    forecasts = get_forecasts()
    forecast_tomorrow = forecasts[tomorrow]

    for forecast in forecast_tomorrow:
        print(forecast)
