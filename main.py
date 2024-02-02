import requests
import datetime as dt
import smtplib
import time


URL_SUN = "https://api.sunrise-sunset.org/json"
URL_ISS = "http://api.open-notify.org/iss-now.json"

# edit with your info
MY_LAT = 16.815304  # edit with your latitude
MY_LNG = 74.569595  # edit with your longitude
MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    response_sun = requests.get(url=URL_SUN, params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()

    sunrise = int(data_sun["results"]["sunrise"].split('T')[1].split(':')[0])
    sunset = int(data_sun["results"]["sunset"].split('T')[1].split(':')[0])

    time_now = dt.datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True


def is_iss_overhead():
    response_iss = requests.get(url=URL_ISS)
    data_iss = response_iss.json()

    iss_lat = float(data_iss["iss_position"]["latitude"])
    iss_lng = float(data_iss["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LNG - 5 <= iss_lng <= MY_LNG + 5:
        return True


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg="Subject:Look Up 🛰️\n\nThe ISS is above in the sky 🔭")


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        send_email()
