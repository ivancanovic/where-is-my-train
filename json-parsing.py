# Loading JSON object from /connections endpoint and parsing relevant nested data for first train to arrive at departure point and going toward specify arrival station
  data = json.loads(response.content)
  delay = data['connection'][0]['departure']['delay']
  platform = data['connection'][0]['departure']['platform']
  canceled = data['connection'][0]['departure']['canceled']
  departure_station = data['connection'][0]['departure']['station']
  arrival_station = data['connection'][0]['arrival']['station']
  vehicle = data['connection'][0]['departure']['vehicleinfo']['shortname']
  departure_time_unix = data['connection'][0]['departure']['time']