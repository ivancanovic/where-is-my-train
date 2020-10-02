 # We will receive two stations as response from Twilio, seperated by blank space, so we need to split those and forward it to API call as two different params
  sms_fetch = request.values['Body']
  station = sms_fetch.split()