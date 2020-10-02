from flask import Flask, request
import json
import requests
import datetime
from datetime import date
from pytz import timezone
import sms-fetch
import today
import json-parsing
import delay
import time-formating

@app.route("/whereismytrain", methods=['GET', 'POST'])
def whereismytrain():

  # Sending API call to /connection endpoint for specific date, departure and arrival stations for retrieving respons in JSON and english language
  response = requests.get("https://api.irail.be/connections/", params={
    "from": station[0],
    "to" : station[1],
    "timesel": "departure",
    "format": "json",
    "date": journey_date,
    "lang": "en"
  })

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
