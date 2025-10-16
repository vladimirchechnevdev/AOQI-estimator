import os
import time
import requests
import datetime

# function to clear the console
clear = lambda: os.system('cls')

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
    print(f"Afternoon! Choose the night you are interested in to get its AOQI.", "1. This night", "2. Next night", sep="\n")

    # estimating current time, timezone and forecast
    curtime = datetime.datetime.now().time().hour
    timezone = int(time.timezone / -3600)
    forecast = get_data()

    # data for report (in format hours-ws-humidity-caf)
    report_data = [[], [], [], []]

    # choosing the nigh to estimate the AOQI
    while True:
        choice = input()
        mean_AOQI = 0.0

        # this list is necessary to estimate min/max value
        AOQI_list = []

        if choice == "1":

            # index for the upcoming night from 22 to 4 o'clock
            if curtime >= 5 and curtime < 22:

                # clearing the list
                report_data = [[], [], [], []]

                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100

                    AOQI = (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                    mean_AOQI += AOQI
                    AOQI_list.append(AOQI)

                    report_data[0].append((curtime + hour) % 24)
                    report_data[1].append(WS)
                    report_data[2].append(round(RH, 1))
                    report_data[3].append(round(CAF, 1))

                mean_AOQI /= 7
                clear()
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.\nThe highest value is {round(max(AOQI_list), 3)}, the least is {round(min(AOQI_list), 3)}.", "\n")

            # index for the remaining night from now to 4 o'clock (in case it's night already)
            else:

                # clearing the list
                report_data = [[], [], [], []]

                for hour in range((29 - curtime) % 24):
                    WS = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100

                    AOQI = (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                    mean_AOQI += AOQI
                    AOQI_list.append(AOQI)

                    report_data[0].append((curtime + hour) % 24)
                    report_data[1].append(WS)
                    report_data[2].append(round(RH, 1))
                    report_data[3].append(round(CAF, 1))

                mean_AOQI /= (29 - curtime) % 24
                clear()
                print(f"The average Astronomical Observations Quality Index value for the current night is {round(mean_AOQI, 3)}.\nThe highest value is {round(max(AOQI_list), 3)}, the least is {round(min(AOQI_list), 3)}.", "\n")


        elif choice == "2":

            # index for the next night (in case it's night yet)
            if curtime >= 0 and curtime < 5:

                # clearing the list
                report_data = [[], [], [], []]

                # estimating AOQI for the further today's night
                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][22 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100

                    AOQI = (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                    mean_AOQI += AOQI
                    AOQI_list.append(AOQI)

                    report_data[0].append((curtime + hour) % 24)
                    report_data[1].append(WS)
                    report_data[2].append(round(RH, 1))
                    report_data[3].append(round(CAF, 1))

                mean_AOQI /= 7
                clear()
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.\nThe highest value is {round(max(AOQI_list), 3)}, the least is {round(min(AOQI_list), 3)}.", "\n")

            # index for the tomorrow's night
            else:

                # clearing the list
                report_data = [[], [], [], []]

                for hour in range(7):
                    WS = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["wind_speed"]
                    RH = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["relative_humidity"] / 160
                    CAF = forecast["properties"]["timeseries"][46 - curtime + timezone + hour]["data"]["instant"]["details"]["cloud_area_fraction"] / 100

                    AOQI = (1 - RH ** 4) * (1 - CAF ** 3) * max(0, (1 - (WS / 15) ** 4))
                    mean_AOQI += AOQI
                    AOQI_list.append(AOQI)

                    report_data[0].append((curtime + hour) % 24)
                    report_data[1].append(WS)
                    report_data[2].append(round(RH, 1))
                    report_data[3].append(round(CAF, 1))

                mean_AOQI /= 7
                clear()
                print(f"The average Astronomical Observations Quality Index value for the upcoming night is {round(mean_AOQI, 3)}.\nThe highest value is {round(max(AOQI_list), 3)}, the least is {round(min(AOQI_list), 3)}.", "\n")

        elif choice == "3":
            clear()
            print("Here's the report for the choosen night:\n")
            print("Hour | Wind Speed | Humidity | Cloud Fraction")
            print("-----+------------+----------+-----------------")

            for ho, ws, hu, caf in zip(report_data[0], report_data[1], report_data[2], report_data[3]):
                print(f"{ho:>3}  | {ws:>3} m/s    | {hu:>5}%   | {caf:>5}%")

            print()

        else:
            print("Incorrect choice. Enter the number 1-2")

        print("What's next?", "1. This night", "2. Next night", "3. Report", sep='\n')


if __name__ == "__main__":
    main()
