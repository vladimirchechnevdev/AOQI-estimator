import time
import requests
import datetime
import astropy


def get_gps():
    url = "https://ipinfo.io/json"

    response = requests.get(url=url)
    data = response.json()

    gps = data["loc"].split(",")
    lat, lon = float(gps[0]), float(gps[1])

    return lat, lon


def get_weather_forecast(lat, lon):
    url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}'
    headers = {"User-Agent": "MyWeatherApp/1.0"}

    response = requests.get(url=url, headers=headers)
    forecast = response.json()

    return forecast


def get_data():
    lat, lon = get_gps()
    forecast = get_weather_forecast(lat=lat, lon=lon)

    return forecast


def main():
    print(f"Afternoon! Choose the night you are interested in to get its AOQI and explore objects possible for observation. Enter the num.", "1. This night", "2. Next night", sep="\n")

    # estimating current time, timezone and forecast
    curtime = datetime.datetime.now().time().hour
    timezone = int(time.timezone / -3600)
    forecast = get_data()

    # choosing the day to estimate the AOQI
    while True:
        choice = input()
        mean_AOQI = 0.0

        if choice == "1":
            if curtime >= 5 and curtime < 22:

                # estimating AOQI for the further today's night
                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100
                    mean_AOQI += (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                mean_AOQI /= 7
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.")


            else:

                # estimating AOQI for the remaining night
                for hour in range((29 - curtime) % 24):
                    WS = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100
                    mean_AOQI += (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                mean_AOQI /= (29 - curtime) % 24
                print(f"The average Astronomical Observations Quality Index value for the current night is {round(mean_AOQI, 3)}.")


        elif choice == "2":
            if curtime >= 0 and curtime < 5:

                # estimating AOQI for the further today's night
                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100
                    mean_AOQI += (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                mean_AOQI /= 7
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.")


            else:

                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100
                    mean_AOQI += (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                mean_AOQI /= 7
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.")

        else:
            print("Incorrect choice. Enter the number 1-2")


if __name__ == "__main__":
    main()
