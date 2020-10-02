from flask import Flask, request
import json
import requests
import datetime
from datetime import date
from pytz import timezone

app = Flask('bootcamp')

@app.route("/jobs", methods=['GET', 'POST'])
def jobs():
  city = request.values['Body']
  response = requests.get("https://jobs.github.com/positions.json", params={
    'location': city
  })
  data = json.loads(response.content)
  title = data [0]['title']
  company = data [0]['company']
  #job_company = data1['company']
  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>Job for location """ + city + """ with job title {} in the company {}</Message>
  </Response>""".format(title,company)

@app.route("/weather", methods=['GET', 'POST'])
def weather():
  city = request.values['Body']
  response = requests.get("http://api.openweathermap.org/data/2.5/weather", params={
    "q": city,
    "appid": "93d35ffb3f8c84f93596e1988315631e",
    "units": "metric"
  })
  data = json.loads(response.content)
  current_temp = data['main']['temp']
  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>Current temperature in """ + str(city)+ """ is """ + str(current_temp) + """°C</Message>
  </Response>"""


@app.route('/sms', methods=['GET', 'POST'])
def sms():
  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>Hello from Bootcamp!</Message>
  </Response>"""


@app.route("/whereismytrain", methods=['GET', 'POST'])
def whereismytrain():

  # We will receive two stations as response from Twilio, seperated by blank space, so we need to split those and forward it to API call as two different params
  sms_fetch = request.values['Body']
  station = sms_fetch.split()
  
  # Making sure that we always send in params today's date correctly formated in order to avoid fluding with irelevant data for journeys in near future
  today = date.today()
  journey_date = today.strftime("%d%m%y")

  # Sending API call to /connection endpoint for specific date, departure and arrival stations for retrieving respons in JSON and english language
  response = requests.get("https://api.irail.be/connections/", params={
    "from": station[0],
    "to" : station[1],
    "timesel": "departure",
    "format": "json",
    "date": journey_date,
    "lang": "en"
  })

  # Loading JSON object from /connections endpoint and parsing relevant nested data for first train to arrive at departure point and going toward specify arrival station
  data = json.loads(response.content)
  delay = data['connection'][0]['departure']['delay']
  platform = data['connection'][0]['departure']['platform']
  canceled = data['connection'][0]['departure']['canceled']
  departure_station = data['connection'][0]['departure']['station']
  arrival_station = data['connection'][0]['arrival']['station']
  vehicle = data['connection'][0]['departure']['vehicleinfo']['shortname']
  departure_time_unix = data['connection'][0]['departure']['time']

  # Checking if there is a delay, and there is, converting response from seconds to minutes
  delay_check = int(delay)
  if delay_check != 0:
    delay_update = ("delayed " + str(int(delay_check / 60)) + " min")
  else:
    delay_update = "on time"
  
  # Set up proper local timezone (Belgium/CET)
  tz = timezone("CET")
  departure_int = float(departure_time_unix)

  # Convering unix timestamp to readable date 
  departure_time = datetime.datetime.fromtimestamp(departure_int, tz).strftime("%H:%M")

  # Check if the train is canceled - no need to do it earlier in the code as it is extremly rare. Send response according to cancelation status of journey.
  canceled_check = int(canceled)
  if canceled_check == 0:
    return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>Your train with number """ + str(vehicle)+ """ scheduled for departure at """ + str(departure_time)+ """ from """ + str(departure_station)+ """ to """ + str(arrival_station)+ """ is """ + str(delay_update)+ """ and leaving from platform number """ + str(platform)+ """!</Message>
  </Response>"""
  else:
    return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>Your train with number """ + str(vehicle)+ """ from """ + str(station[0])+ """ to """ + str(station[1])+ """ has been canceled!</Message>
  </Response>"""

# app.run(debug=True, host='0.0.0.0', port=8080)
