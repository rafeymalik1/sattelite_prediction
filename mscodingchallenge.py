import requests
from datetime import datetime, timedelta, date


def flyby(longitude, latitude):
    API_KEY = "aXRwHdkCPdvtkbLmc1TqLxJu6JOhnigZCWxvJyJF"
    dates = []
    previous_date = ""

    # this date will be given to the API, which will then return the date of the image taken that is closest to this one
    # this is the initial date range and every next range will be before this one
    range_date = '2022-01-01'

    # this while loop will run until we get a sample of 6 dates
    # the reason we do this is to get a rough idea of the past dates so we can calculate avg_time_delta
    # the number 6 is arbitrary, but should be good enough to get an accurate time delta
    while len(dates) < 6:

        # API call
        URL = 'https://api.nasa.gov/planetary/earth/assets?lon=' + longitude + \
            '&lat=' + latitude + '&date=' + range_date + '&&dim=0.10&api_key=' + API_KEY
        response = requests.get(URL)
        # this stores the most recent date that was requested from the API
        current_date = response.json()['date'][:10]

        # appending the most recent date to the dates list unless it is already in the list
        if current_date != previous_date:
            dates.append(current_date)
            # if this goes through then we update previous_date for the next iteration
            previous_date = current_date

        # after every iteration of the loop, we move the range date back by 7 days
        # 7 days should be precise enough since the satellite does not make a trip in any fewer amount of time
        range_date = str(date.fromisoformat(range_date) - timedelta(7))

    # the following block of code calculates the difference between each adjacent date in the dates list
    # and appends it to a list "times_delta"
    times_delta = []
    for i in range(1, len(dates)):
        d1 = str(dates[i])
        d2 = str(dates[i-1])
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        times_delta.append(abs((d2 - d1).days))

    # calculating the average amount of time between images
    avg_time_delta = round(sum(times_delta)/len(times_delta))

    # converting the latest date into the proper format for the upcoming calculation
    last_date = datetime.strptime(dates[0], "%Y-%m-%d")

    # the next estimated time is calculated by adding the latest date to the average date in between dates
    print("The estimated date for when the next picture will be taken at this location is " +
          str((last_date + timedelta(avg_time_delta)))[:10] + ".")


def main():
    lon_inp = input("Input the longitude of the location: ")
    lat_inp = input("Input the latitude of the location: ")
    flyby(lon_inp, lat_inp)


if __name__ == '__main__':
    main()