# Set up proper local timezone (Belgium/CET)
  tz = timezone("CET")
  departure_int = float(departure_time_unix)

  # Convering unix timestamp to readable date 
  departure_time = datetime.datetime.fromtimestamp(departure_int, tz).strftime("%H:%M")